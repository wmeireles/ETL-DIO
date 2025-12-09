# 🚀 Guia de Início Rápido

## Instalação em 3 passos

### 1. Clone e prepare o ambiente
```bash
git clone <seu-repo>
cd "ETL DIO"
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure variáveis (opcional para modo mock)
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env

# Edite .env e adicione sua OPENAI_API_KEY (apenas para modo real)
```

### 3. Execute!

#### Modo Mock (recomendado para começar)
```bash
python -m src.etl.main --csv SDW2023.csv --mode mock
```

#### Modo Real (requer OPENAI_API_KEY)
```bash
python -m src.etl.main --csv SDW2023.csv --mode real
```

## 🧪 Testando

```bash
# Executar todos os testes
pytest

# Com cobertura
pytest --cov=src.etl

# Apenas um arquivo
pytest tests/test_extract.py -v
```

## 🔧 Usando Mock Server (se API real estiver offline)

Terminal 1 - Inicie o servidor:
```bash
pip install flask
python scripts/mock_server.py
```

Terminal 2 - Execute o ETL:
```bash
python -m src.etl.main --csv SDW2023.csv --mode mock --api-url http://localhost:5000
```

## 📝 Exemplos de Uso

### Dry Run (não atualiza nada)
```bash
python -m src.etl.main --csv SDW2023.csv --mode mock --dry-run
```

### Com logs detalhados
```bash
python -m src.etl.main --csv SDW2023.csv --mode mock --log-level DEBUG
```

### Criar seu próprio CSV
```csv
UserID
1
2
3
```

Salve como `meus_usuarios.csv` e execute:
```bash
python -m src.etl.main --csv meus_usuarios.csv --mode mock
```

## ❓ Problemas Comuns

### "ModuleNotFoundError: No module named 'src'"
Execute sempre com `python -m src.etl.main` (não `python src/etl/main.py`)

### "OPENAI_API_KEY não configurada"
Use `--mode mock` ou configure a chave no arquivo `.env`

### "Connection refused" ou timeout
A API pode estar offline. Use o mock server ou `--mode mock`

## 📚 Próximos Passos

1. Leia o [README.md](README.md) completo
2. Explore os testes em `tests/`
3. Customize mensagens em `src/etl/transform.py`
4. Adicione seus próprios usuários no CSV
