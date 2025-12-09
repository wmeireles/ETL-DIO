"""Módulo de extração de dados"""
import logging
import pandas as pd
import requests
from typing import List, Optional, Dict, Any
from src.etl.config import SDW_API_URL, HTTP_TIMEOUT
from src.etl.utils import retry_with_backoff

logger = logging.getLogger("etl")

def read_csv(file_path: str) -> List[int]:
    """
    Lê arquivo CSV e extrai lista de UserIDs
    
    Args:
        file_path: Caminho do arquivo CSV
        
    Returns:
        Lista de IDs de usuários
    """
    try:
        df = pd.read_csv(file_path)
        user_ids = df['UserID'].dropna().astype(int).tolist()
        logger.info(f"Lidos {len(user_ids)} IDs do arquivo {file_path}")
        return user_ids
    except Exception as e:
        logger.error(f"Erro ao ler CSV {file_path}: {e}")
        raise

@retry_with_backoff()
def get_user(user_id: int, api_url: str = SDW_API_URL) -> Optional[Dict[str, Any]]:
    """
    Busca dados de um usuário na API
    
    Args:
        user_id: ID do usuário
        api_url: URL base da API
        
    Returns:
        Dados do usuário ou None se não encontrado
    """
    url = f"{api_url}/users/{user_id}"
    
    try:
        response = requests.get(url, timeout=HTTP_TIMEOUT)
        
        if response.status_code == 200:
            user = response.json()
            logger.info(f"Usuário {user_id} obtido com sucesso: {user.get('name', 'N/A')}")
            return user
        elif response.status_code == 404:
            logger.warning(f"Usuário {user_id} não encontrado (404)")
            return None
        else:
            logger.error(f"Erro ao buscar usuário {user_id}: status {response.status_code}")
            response.raise_for_status()
            
    except requests.exceptions.Timeout:
        logger.error(f"Timeout ao buscar usuário {user_id}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de requisição ao buscar usuário {user_id}: {e}")
        raise

def extract_users(user_ids: List[int], api_url: str = SDW_API_URL) -> List[Dict[str, Any]]:
    """
    Extrai dados de múltiplos usuários
    
    Args:
        user_ids: Lista de IDs
        api_url: URL base da API
        
    Returns:
        Lista de usuários válidos
    """
    users = []
    
    for user_id in user_ids:
        try:
            user = get_user(user_id, api_url)
            if user:
                users.append(user)
        except Exception as e:
            logger.error(f"Pulando usuário {user_id} devido a erro: {e}")
            continue
    
    logger.info(f"Total de {len(users)} usuários extraídos com sucesso")
    return users
