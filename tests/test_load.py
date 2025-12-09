"""Testes do módulo load"""
import pytest
from unittest.mock import Mock, patch
from src.etl.load import (
    is_duplicate_news,
    add_news_to_user,
    update_user,
    load_users
)

def test_is_duplicate_news_true():
    """Testa detecção de notícia duplicada"""
    user = {
        "id": 1,
        "news": [
            {"icon": "url", "description": "Mensagem existente"}
        ]
    }
    
    assert is_duplicate_news(user, "Mensagem existente") is True

def test_is_duplicate_news_false():
    """Testa notícia não duplicada"""
    user = {
        "id": 1,
        "news": [
            {"icon": "url", "description": "Mensagem existente"}
        ]
    }
    
    assert is_duplicate_news(user, "Nova mensagem") is False

def test_add_news_to_user_new():
    """Testa adição de nova notícia"""
    user = {"id": 1, "name": "User", "news": []}
    message = "Nova mensagem de investimento"
    
    updated = add_news_to_user(user, message)
    
    assert len(updated["news"]) == 1
    assert updated["news"][0]["description"] == message
    assert updated["_skipped"] is False

def test_add_news_to_user_duplicate():
    """Testa que notícia duplicada não é adicionada"""
    user = {
        "id": 1,
        "news": [{"description": "Mensagem existente"}]
    }
    
    updated = add_news_to_user(user, "Mensagem existente")
    
    assert len(updated["news"]) == 1
    assert updated["_skipped"] is True

@patch('src.etl.load.requests.put')
def test_update_user_success(mock_put):
    """Testa atualização bem-sucedida"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_put.return_value = mock_response
    
    user = {"id": 1, "name": "User", "news": []}
    
    result = update_user(user)
    
    assert result is True

def test_update_user_dry_run():
    """Testa dry run (não faz requisição)"""
    user = {"id": 1, "name": "User"}
    
    result = update_user(user, dry_run=True)
    
    assert result is True

def test_update_user_skipped():
    """Testa usuário marcado como skipped"""
    user = {"id": 1, "_skipped": True}
    
    result = update_user(user)
    
    assert result is True

@patch('src.etl.load.update_user')
def test_load_users(mock_update):
    """Testa carregamento de múltiplos usuários"""
    mock_update.return_value = True
    
    users = [
        {"id": 1, "name": "User 1", "generated_message": "Msg 1", "news": []},
        {"id": 2, "name": "User 2", "generated_message": "Msg 2", "news": []}
    ]
    
    stats = load_users(users)
    
    assert stats["success"] == 2
    assert stats["failed"] == 0
