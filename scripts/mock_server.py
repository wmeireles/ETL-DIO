"""
Mock Server para simular a API Santander Dev Week
Útil quando a API real está indisponível
"""
from flask import Flask, jsonify, request
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Dados mock de usuários
MOCK_USERS = {
    1: {
        "id": 1,
        "name": "João Silva",
        "account": {"number": "12345-6", "agency": "0001"},
        "card": {"number": "**** 1234", "limit": 5000.0},
        "features": [],
        "news": []
    },
    2: {
        "id": 2,
        "name": "Maria Santos",
        "account": {"number": "23456-7", "agency": "0001"},
        "card": {"number": "**** 2345", "limit": 8000.0},
        "features": [],
        "news": []
    },
    3: {
        "id": 3,
        "name": "Carlos Oliveira",
        "account": {"number": "34567-8", "agency": "0001"},
        "card": {"number": "**** 3456", "limit": 10000.0},
        "features": [],
        "news": []
    },
    4: {
        "id": 4,
        "name": "Ana Costa",
        "account": {"number": "45678-9", "agency": "0001"},
        "card": {"number": "**** 4567", "limit": 6000.0},
        "features": [],
        "news": []
    },
    5: {
        "id": 5,
        "name": "Pedro Alves",
        "account": {"number": "56789-0", "agency": "0001"},
        "card": {"number": "**** 5678", "limit": 7500.0},
        "features": [],
        "news": []
    }
}

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retorna dados de um usuário"""
    user = MOCK_USERS.get(user_id)
    
    if user:
        app.logger.info(f"GET /users/{user_id} - 200 OK")
        return jsonify(user), 200
    else:
        app.logger.warning(f"GET /users/{user_id} - 404 Not Found")
        return jsonify({"error": "User not found"}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Atualiza dados de um usuário"""
    if user_id not in MOCK_USERS:
        app.logger.warning(f"PUT /users/{user_id} - 404 Not Found")
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    MOCK_USERS[user_id] = data
    
    app.logger.info(f"PUT /users/{user_id} - 200 OK")
    app.logger.debug(f"Updated data: {data}")
    
    return jsonify(data), 200

@app.route('/users', methods=['GET'])
def list_users():
    """Lista todos os usuários"""
    return jsonify(list(MOCK_USERS.values())), 200

if __name__ == '__main__':
    print("=" * 60)
    print("Mock Server - Santander Dev Week API")
    print("=" * 60)
    print("Servidor rodando em: http://localhost:5000")
    print("\nEndpoints disponíveis:")
    print("  GET  /users/<id>  - Buscar usuário")
    print("  PUT  /users/<id>  - Atualizar usuário")
    print("  GET  /users       - Listar todos")
    print("\nPara usar no ETL, configure:")
    print("  --api-url http://localhost:5000")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
