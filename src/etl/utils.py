"""Funções utilitárias"""
import logging
import time
from functools import wraps
from typing import Callable, Any
from src.etl.config import MAX_RETRIES, RETRY_BACKOFF_FACTOR

def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configura logging do projeto"""
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger("etl")

def retry_with_backoff(max_retries: int = MAX_RETRIES, backoff_factor: int = RETRY_BACKOFF_FACTOR):
    """
    Decorator para retry com backoff exponencial
    
    Args:
        max_retries: Número máximo de tentativas
        backoff_factor: Fator de multiplicação do delay
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = logging.getLogger("etl")
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"{func.__name__} falhou após {max_retries} tentativas: {e}")
                        raise
                    delay = backoff_factor ** attempt
                    logger.warning(f"{func.__name__} falhou (tentativa {attempt + 1}/{max_retries}). Retry em {delay}s: {e}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

def truncate_message(message: str, max_length: int = 100) -> str:
    """
    Trunca mensagem respeitando limite de caracteres sem cortar palavras
    
    Args:
        message: Mensagem original
        max_length: Tamanho máximo
        
    Returns:
        Mensagem truncada
    """
    if len(message) <= max_length:
        return message
    
    truncated = message[:max_length]
    last_space = truncated.rfind(' ')
    
    if last_space > max_length * 0.8:  # Se o último espaço está em posição razoável
        return truncated[:last_space].rstrip('.,!?;:') + '...'
    
    return truncated[:max_length-3] + '...'
