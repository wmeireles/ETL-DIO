# 📋 Exemplos de Payloads e Respostas

## GET /users/{id} - Resposta de Sucesso (200)

```json
{
  "id": 1,
  "name": "João Silva",
  "account": {
    "id": 1,
    "number": "12345-6",
    "agency": "0001",
    "balance": 1500.50,
    "limit": 5000.00
  },
  "card": {
    "id": 1,
    "number": "**** **** **** 1234",
    "limit": 3000.00
  },
  "features": [
    {
      "id": 1,
      "icon": "https://example.com/icon.svg",
      "description": "Feature 1"
    }
  ],
  "news": [
    {
      "id": 1,
      "icon": "https://example.com/news-icon.svg",
      "description": "Notícia antiga existente"
    }
  ]
}
```

## GET /users/{id} - Usuário Não Encontrado (404)

```json
{
  "error": "User not found",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## PUT /users/{id} - Payload de Atualização

```json
{
  "id": 1,
  "name": "João Silva",
  "account": {
    "id": 1,
    "number": "12345-6",
    "agency": "0001",
    "balance": 1500.50,
    "limit": 5000.00
  },
  "card": {
    "id": 1,
    "number": "**** **** **** 1234",
    "limit": 3000.00
  },
  "features": [
    {
      "id": 1,
      "icon": "https://example.com/icon.svg",
      "description": "Feature 1"
    }
  ],
  "news": [
    {
      "id": 1,
      "icon": "https://example.com/news-icon.svg",
      "description": "Notícia antiga existente"
    },
    {
      "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
      "description": "João, investir hoje é essencial para o seu futuro. Saiba mais!"
    }
  ]
}
```

## PUT /users/{id} - Resposta de Sucesso (200)

```json
{
  "id": 1,
  "name": "João Silva",
  "account": {
    "id": 1,
    "number": "12345-6",
    "agency": "0001",
    "balance": 1500.50,
    "limit": 5000.00
  },
  "card": {
    "id": 1,
    "number": "**** **** **** 1234",
    "limit": 3000.00
  },
  "features": [
    {
      "id": 1,
      "icon": "https://example.com/icon.svg",
      "description": "Feature 1"
    }
  ],
  "news": [
    {
      "id": 1,
      "icon": "https://example.com/news-icon.svg",
      "description": "Notícia antiga existente"
    },
    {
      "id": 2,
      "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
      "description": "João, investir hoje é essencial para o seu futuro. Saiba mais!"
    }
  ]
}
```

## Exemplos de Mensagens Geradas

### Modo Mock
```
João, investir hoje é essencial para o seu futuro. Saiba mais!
Maria, investir hoje é essencial para o seu futuro. Saiba mais!
Carlos, investir hoje é essencial para o seu futuro. Saiba mais!
```

### Modo Real (OpenAI GPT-4)
```
João, comece a investir hoje e garanta seu futuro financeiro!
Maria, seus investimentos podem transformar seus sonhos em realidade.
Carlos, invista agora e colha os frutos amanhã. Fale conosco!
```

## Exemplo de Execução Completa

### Entrada (SDW2023.csv)
```csv
UserID
1
2
3
```

### Saída no Console (modo mock)
```
2024-01-15 10:30:00 - etl - INFO - ============================================================
2024-01-15 10:30:00 - etl - INFO - Iniciando Pipeline ETL - Santander Dev Week 2023
2024-01-15 10:30:00 - etl - INFO - Modo: MOCK
2024-01-15 10:30:00 - etl - INFO - CSV: SDW2023.csv
2024-01-15 10:30:00 - etl - INFO - API URL: https://sdw-2023-prd.up.railway.app
2024-01-15 10:30:00 - etl - INFO - Dry Run: False
2024-01-15 10:30:00 - etl - INFO - ============================================================

2024-01-15 10:30:00 - etl - INFO - [EXTRACT] Iniciando extração de dados...
2024-01-15 10:30:00 - etl - INFO - Lidos 3 IDs do arquivo SDW2023.csv
2024-01-15 10:30:01 - etl - INFO - Usuário 1 obtido com sucesso: João Silva
2024-01-15 10:30:02 - etl - INFO - Usuário 2 obtido com sucesso: Maria Santos
2024-01-15 10:30:03 - etl - INFO - Usuário 3 obtido com sucesso: Carlos Oliveira
2024-01-15 10:30:03 - etl - INFO - Total de 3 usuários extraídos com sucesso

2024-01-15 10:30:03 - etl - INFO - [TRANSFORM] Iniciando transformação e geração de mensagens...
2024-01-15 10:30:03 - etl - INFO - Mensagem mock gerada para João Silva: João, investir hoje é essencial para o seu futuro. Saiba mais!
2024-01-15 10:30:03 - etl - INFO - Mensagem mock gerada para Maria Santos: Maria, investir hoje é essencial para o seu futuro. Saiba mais!
2024-01-15 10:30:03 - etl - INFO - Mensagem mock gerada para Carlos Oliveira: Carlos, investir hoje é essencial para o seu futuro. Saiba mais!
2024-01-15 10:30:03 - etl - INFO - Mensagens geradas: 3/3

2024-01-15 10:30:03 - etl - INFO - [LOAD] Iniciando carregamento e atualização...
2024-01-15 10:30:03 - etl - INFO - Notícia adicionada ao usuário 1: João, investir hoje é essencial para o seu futuro. Saiba mais!
2024-01-15 10:30:04 - etl - INFO - Usuário 1 atualizado com sucesso
2024-01-15 10:30:04 - etl - INFO - Notícia adicionada ao usuário 2: Maria, investir hoje é essencial para o seu futuro. Saiba mais!
2024-01-15 10:30:05 - etl - INFO - Usuário 2 atualizado com sucesso
2024-01-15 10:30:05 - etl - INFO - Notícia adicionada ao usuário 3: Carlos, investir hoje é essencial para o seu futuro. Saiba mais!
2024-01-15 10:30:06 - etl - INFO - Usuário 3 atualizado com sucesso
2024-01-15 10:30:06 - etl - INFO - Carregamento concluído - Sucesso: 3, Falha: 0, Pulados: 0

2024-01-15 10:30:06 - etl - INFO - ============================================================
2024-01-15 10:30:06 - etl - INFO - Pipeline ETL concluído!
2024-01-15 10:30:06 - etl - INFO - Total de usuários processados: 3
2024-01-15 10:30:06 - etl - INFO - Atualizações bem-sucedidas: 3
2024-01-15 10:30:06 - etl - INFO - Atualizações falhadas: 0
2024-01-15 10:30:06 - etl - INFO - Atualizações puladas: 0
2024-01-15 10:30:06 - etl - INFO - ============================================================
```
