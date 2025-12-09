"""Testes do módulo transform"""
import pytest
from unittest.mock import Mock, patch
from src.etl.transform import (
    generate_message_mock,
    generate_message_openai,
    generate_message,
    transform_users
)

def test_generate_message_mock():
    """Testa geração de mensagem mock"""
    user = {"id": 1, "name": "João Silva"}
    
    message = generate_message_mock(user)
    
    assert message is not None
    assert len(message) <= 100
    assert "João" in message
    assert "investir" in message.lower()

def test_generate_message_mock_no_name():
    """Testa mensagem mock sem nome"""
    user = {"id": 1}
    
    message = generate_message_mock(user)
    
    assert message is not None
    assert len(message) <= 100

@patch('src.etl.transform.OpenAI')
def test_generate_message_openai(mock_openai_class):
    """Testa geração via OpenAI"""
    mock_client = Mock()
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="Invista no seu futuro hoje!"))]
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai_class.return_value = mock_client
    
    user = {"id": 1, "name": "Maria"}
    
    with patch('src.etl.transform.OPENAI_API_KEY', 'test-key'):
        message = generate_message_openai(user)
    
    assert message == "Invista no seu futuro hoje!"
    assert len(message) <= 100

def test_generate_message_mode_mock():
    """Testa generate_message em modo mock"""
    user = {"id": 1, "name": "Carlos"}
    
    message = generate_message(user, mode="mock")
    
    assert message is not None
    assert len(message) <= 100

@patch('src.etl.transform.generate_message_openai')
def test_generate_message_fallback(mock_openai):
    """Testa fallback para mock quando OpenAI falha"""
    mock_openai.side_effect = Exception("API Error")
    user = {"id": 1, "name": "Ana"}
    
    message = generate_message(user, mode="real")
    
    assert message is not None
    assert "Ana" in message

def test_transform_users():
    """Testa transformação de lista de usuários"""
    users = [
        {"id": 1, "name": "User 1"},
        {"id": 2, "name": "User 2"}
    ]
    
    transformed = transform_users(users, mode="mock")
    
    assert len(transformed) == 2
    assert all('generated_message' in u for u in transformed)
    assert all(u['generated_message'] is not None for u in transformed)
