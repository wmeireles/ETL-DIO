"""Testes do módulo extract"""
import pytest
from unittest.mock import Mock, patch, mock_open
from src.etl.extract import read_csv, get_user, extract_users

def test_read_csv_success(tmp_path):
    """Testa leitura bem-sucedida do CSV"""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("UserID\n1\n2\n3\n")
    
    user_ids = read_csv(str(csv_file))
    
    assert user_ids == [1, 2, 3]
    assert len(user_ids) == 3

def test_read_csv_empty(tmp_path):
    """Testa CSV vazio"""
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("UserID\n")
    
    user_ids = read_csv(str(csv_file))
    
    assert user_ids == []

@patch('src.etl.extract.requests.get')
def test_get_user_success(mock_get):
    """Testa busca de usuário bem-sucedida"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "name": "João Silva",
        "news": []
    }
    mock_get.return_value = mock_response
    
    user = get_user(1)
    
    assert user is not None
    assert user["id"] == 1
    assert user["name"] == "João Silva"

@patch('src.etl.extract.requests.get')
def test_get_user_not_found(mock_get):
    """Testa usuário não encontrado (404)"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    user = get_user(999)
    
    assert user is None

@patch('src.etl.extract.get_user')
def test_extract_users(mock_get_user):
    """Testa extração de múltiplos usuários"""
    mock_get_user.side_effect = [
        {"id": 1, "name": "User 1"},
        {"id": 2, "name": "User 2"},
        None  # Usuário 3 não encontrado
    ]
    
    users = extract_users([1, 2, 3])
    
    assert len(users) == 2
    assert users[0]["id"] == 1
    assert users[1]["id"] == 2
