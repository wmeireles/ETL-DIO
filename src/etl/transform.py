"""Módulo de transformação e geração de mensagens"""
import logging
from typing import Dict, Any
from openai import OpenAI
from src.etl.config import (
    OPENAI_API_KEY, 
    OPENAI_MODEL, 
    SYSTEM_PROMPT, 
    MAX_MESSAGE_LENGTH,
    OPENAI_TIMEOUT
)
from src.etl.utils import retry_with_backoff, truncate_message

logger = logging.getLogger("etl")

@retry_with_backoff()
def generate_message_openai(user: Dict[str, Any]) -> str:
    """
    Gera mensagem usando OpenAI GPT-4
    
    Args:
        user: Dados do usuário
        
    Returns:
        Mensagem personalizada
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY não configurada")
    
    client = OpenAI(api_key=OPENAI_API_KEY, timeout=OPENAI_TIMEOUT)
    user_name = user.get('name', 'Cliente')
    
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Cliente: {user_name}"}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        message = response.choices[0].message.content.strip()
        message = truncate_message(message, MAX_MESSAGE_LENGTH)
        
        logger.info(f"Mensagem gerada via OpenAI para {user_name}: {message}")
        return message
        
    except Exception as e:
        logger.error(f"Erro ao gerar mensagem via OpenAI para {user_name}: {e}")
        raise

def generate_message_mock(user: Dict[str, Any]) -> str:
    """
    Gera mensagem mock (sem API externa)
    
    Args:
        user: Dados do usuário
        
    Returns:
        Mensagem personalizada mock
    """
    user_name = user.get('name', 'Cliente')
    first_name = user_name.split()[0] if user_name else 'Cliente'
    
    message = f"{first_name}, investir hoje é essencial para o seu futuro. Saiba mais!"
    message = truncate_message(message, MAX_MESSAGE_LENGTH)
    
    logger.info(f"Mensagem mock gerada para {user_name}: {message}")
    return message

def generate_message(user: Dict[str, Any], mode: str = "mock") -> str:
    """
    Gera mensagem personalizada (real ou mock)
    
    Args:
        user: Dados do usuário
        mode: "real" para OpenAI, "mock" para local
        
    Returns:
        Mensagem personalizada
    """
    if not user.get('name'):
        logger.warning(f"Usuário sem nome: {user.get('id', 'N/A')}")
    
    try:
        if mode == "real":
            return generate_message_openai(user)
        else:
            return generate_message_mock(user)
    except Exception as e:
        logger.warning(f"Fallback para mock devido a erro: {e}")
        return generate_message_mock(user)

def transform_users(users: list[Dict[str, Any]], mode: str = "mock") -> list[Dict[str, Any]]:
    """
    Transforma lista de usuários adicionando mensagens
    
    Args:
        users: Lista de usuários
        mode: Modo de geração ("real" ou "mock")
        
    Returns:
        Lista de usuários com mensagens geradas
    """
    for user in users:
        try:
            message = generate_message(user, mode)
            user['generated_message'] = message
        except Exception as e:
            logger.error(f"Erro ao gerar mensagem para usuário {user.get('id')}: {e}")
            user['generated_message'] = None
    
    successful = sum(1 for u in users if u.get('generated_message'))
    logger.info(f"Mensagens geradas: {successful}/{len(users)}")
    
    return users
