"""Módulo de carregamento e atualização de dados"""
import logging
import requests
from typing import Dict, Any
from src.etl.config import SDW_API_URL, HTTP_TIMEOUT, NEWS_ICON_URL
from src.etl.utils import retry_with_backoff

logger = logging.getLogger("etl")

def is_duplicate_news(user: Dict[str, Any], description: str) -> bool:
    """
    Verifica se a notícia já existe (idempotência)
    
    Args:
        user: Dados do usuário
        description: Descrição da notícia
        
    Returns:
        True se já existe, False caso contrário
    """
    news_list = user.get('news', [])
    
    for news in news_list:
        if news.get('description') == description:
            return True
    
    return False

def add_news_to_user(user: Dict[str, Any], message: str) -> Dict[str, Any]:
    """
    Adiciona notícia ao usuário (se não duplicada)
    
    Args:
        user: Dados do usuário
        message: Mensagem a adicionar
        
    Returns:
        Usuário atualizado
    """
    if is_duplicate_news(user, message):
        logger.info(f"Notícia duplicada para usuário {user.get('id')} - pulando")
        user['_skipped'] = True
        return user
    
    if 'news' not in user:
        user['news'] = []
    
    news_item = {
        "icon": NEWS_ICON_URL,
        "description": message
    }
    
    user['news'].append(news_item)
    user['_skipped'] = False
    
    logger.info(f"Notícia adicionada ao usuário {user.get('id')}: {message}")
    return user

@retry_with_backoff()
def update_user(user: Dict[str, Any], api_url: str = SDW_API_URL, dry_run: bool = False) -> bool:
    """
    Atualiza usuário na API via PUT
    
    Args:
        user: Dados do usuário
        api_url: URL base da API
        dry_run: Se True, não faz a requisição real
        
    Returns:
        True se sucesso, False caso contrário
    """
    user_id = user.get('id')
    
    if dry_run:
        logger.info(f"[DRY RUN] Usuário {user_id} seria atualizado")
        return True
    
    if user.get('_skipped'):
        logger.info(f"Usuário {user_id} pulado (notícia duplicada)")
        return True
    
    url = f"{api_url}/users/{user_id}"
    
    # Remove campos internos antes de enviar
    payload = {k: v for k, v in user.items() if not k.startswith('_')}
    
    try:
        response = requests.put(url, json=payload, timeout=HTTP_TIMEOUT)
        
        if response.status_code == 200:
            logger.info(f"Usuário {user_id} atualizado com sucesso")
            return True
        else:
            logger.error(f"Erro ao atualizar usuário {user_id}: status {response.status_code}")
            response.raise_for_status()
            return False
            
    except requests.exceptions.Timeout:
        logger.error(f"Timeout ao atualizar usuário {user_id}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de requisição ao atualizar usuário {user_id}: {e}")
        raise

def load_users(users: list[Dict[str, Any]], api_url: str = SDW_API_URL, dry_run: bool = False) -> Dict[str, int]:
    """
    Carrega/atualiza múltiplos usuários
    
    Args:
        users: Lista de usuários
        api_url: URL base da API
        dry_run: Se True, não faz requisições reais
        
    Returns:
        Estatísticas de sucesso/falha
    """
    stats = {"success": 0, "failed": 0, "skipped": 0}
    
    for user in users:
        if not user.get('generated_message'):
            logger.warning(f"Usuário {user.get('id')} sem mensagem - pulando")
            stats["skipped"] += 1
            continue
        
        # Adiciona notícia ao usuário
        user = add_news_to_user(user, user['generated_message'])
        
        if user.get('_skipped'):
            stats["skipped"] += 1
            continue
        
        try:
            success = update_user(user, api_url, dry_run)
            if success:
                stats["success"] += 1
            else:
                stats["failed"] += 1
        except Exception as e:
            logger.error(f"Erro ao processar usuário {user.get('id')}: {e}")
            stats["failed"] += 1
    
    logger.info(f"Carregamento concluído - Sucesso: {stats['success']}, Falha: {stats['failed']}, Pulados: {stats['skipped']}")
    return stats
