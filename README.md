# Projeto ETL

Pipeline ETL em Python que gera e envia mensagens de marketing personalizadas sobre investimentos para clientes.

## 📋 Descrição

Este projeto implementa um pipeline ETL que:
1. **Extract**: Lê IDs de usuários de um arquivo CSV
2. **Transform**: Busca dados dos usuários na API e gera mensagens personalizadas usando OpenAI GPT-4
3. **Load**: Atualiza os usuários com as novas mensagens via API REST

## 🏗️ Arquitetura

```
CSV (IDs) → Extract → API GET (user data) → Transform (OpenAI) → Load → API PUT (update)
```

**Componentes principais:**
- `extract.py`: Leitura do CSV e busca de dados via API
- `transform.py`: Geração de mensagens personalizadas (OpenAI ou mock)
- `load.py`: Atualização dos usuários via API
- `config.py`: Configurações e variáveis de ambiente
- `utils.py`: Funções auxiliares (retries, logging)

## 📁 Estrutura do Projeto

```
ETL DIO/
├── src/
│   └── etl/
│       ├── __init__.py
│       ├── main.py          # Entry point
│       ├── extract.py       # Extração de dados
│       ├── transform.py     # Transformação e geração de mensagens
│       ├── load.py          # Carregamento/atualização
│       ├── config.py        # Configurações
│       └── utils.py         # Utilitários (retries, logging)
├── tests/
│   ├── __init__.py
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── scripts/
│   └── mock_server.py       # Servidor mock para testes
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI
├── SDW2023.csv              # Arquivo de entrada (exemplo)
├── .env.example             # Exemplo de variáveis de ambiente
├── requirements.txt         # Dependências
└── README.md
```

## 🚀 Como Rodar

### Pré-requisitos

- Python 3.10+
- pip

### Instalação

1. Clone o repositório:
```bash
git clone <seu-repo>
cd "ETL DIO"
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
# Copie o arquivo de exemplo
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# Edite o .env e adicione sua chave da OpenAI (apenas para modo real)
```

### Execução

#### Modo Mock (sem APIs externas - recomendado para testes)
```bash
python -m src.etl.main --csv SDW2023.csv --mode mock
```

#### Modo Real (com OpenAI e API externa)
```bash
python -m src.etl.main --csv SDW2023.csv --mode real
```

#### Dry Run (não faz atualizações)
```bash
python -m src.etl.main --csv SDW2023.csv --mode mock --dry-run
```

### Executar Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src.etl tests/

# Verbose
pytest -v
```

### Executar Linter

```bash
flake8 src/ tests/
```

## 📊 Exemplo de Dados

### SDW2023.csv (entrada)
```csv
UserID
1
2
3
```

### Resposta da API GET /users/{id}
```json
{
  "id": 1,
  "name": "João Silva",
  "account": {
    "number": "12345-6",
    "agency": "0001"
  },
  "news": []
}
```

### Payload PUT /users/{id} (atualização)
```json
{
  "id": 1,
  "name": "João Silva",
  "account": {
    "number": "12345-6",
    "agency": "0001"
  },
  "news": [
    {
      "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
      "description": "João, investir hoje é essencial para o seu futuro. Saiba mais!"
    }
  ]
}
```

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```env
OPENAI_API_KEY=sk-...
SDW_API_URL=https://sdw-2023-prd.up.railway.app
LOG_LEVEL=INFO
```

## 🧪 Testes

O projeto inclui testes unitários para:
- ✅ Leitura do CSV
- ✅ Busca de usuários (mock)
- ✅ Geração de mensagens (mock e real)
- ✅ Atualização de usuários (mock)
- ✅ Lógica de idempotência
- ✅ Tratamento de erros e retries

## 🔒 Segurança

- Chaves de API armazenadas em `.env` (não commitado)
- Timeout em todas as chamadas HTTP
- Retries com backoff exponencial
- Validação de entrada

## 📈 Decisões de Design

1. **Separação ETL**: Código organizado em extract/transform/load para clareza e testabilidade
2. **Modo Mock**: Permite testes sem dependências externas
3. **Idempotência**: Verifica duplicatas antes de adicionar notícias
4. **Retries**: Implementa backoff exponencial para resiliência
5. **Logging**: Rastreamento completo de operações
6. **Dry Run**: Permite validação sem modificar dados

## 🚧 Limitações Conhecidas

- API externa pode estar indisponível (use modo mock ou mock_server.py)
- Mensagens limitadas a 100 caracteres
- Sem persistência de estado entre execuções

## 🔮 Extensões Futuras

1. **Segmentação de clientes**: Mensagens diferentes por perfil
2. **A/B Testing**: Testar variações de mensagens
3. **Fila de processamento**: Usar Celery/RabbitMQ para escala
4. **Métricas e telemetria**: Integração com Prometheus/Grafana
5. **Dashboard**: Visualização de resultados
6. **Banco de dados**: Persistir histórico de mensagens
7. **Rate limiting**: Controle de taxa de requisições
8. **Webhooks**: Notificações de conclusão

## 📝 Licença

MIT

