"""Configurações do projeto"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SDW_API_URL = os.getenv("SDW_API_URL", "https://sdw-2023-prd.up.railway.app")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# HTTP Configuration
HTTP_TIMEOUT = 10
OPENAI_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_BACKOFF_FACTOR = 2

# Message Configuration
MAX_MESSAGE_LENGTH = 100
NEWS_ICON_URL = "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg"

# OpenAI Configuration
OPENAI_MODEL = "gpt-4"
SYSTEM_PROMPT = (
    "Você é um especialista em marketing bancário. "
    "Escreva UMA mensagem curta, cordial, pessoal e persuasiva sobre a importância dos investimentos. "
    "Máximo 100 caracteres. Use o nome do cliente quando fizer sentido."
)
