# 🚀 Guia de Deploy

## Opções de Deploy

Este projeto pode ser deployado em diversos ambientes. Abaixo estão as opções mais comuns.

---

## 1. Deploy Local (Desenvolvimento)

### Pré-requisitos
- Python 3.10+
- Git

### Passos

```bash
# 1. Clone o repositório
git clone <seu-repo>
cd "ETL DIO"

# 2. Execute setup
bash scripts/setup.sh  # Linux/Mac
scripts\setup.bat      # Windows

# 3. Configure .env
cp .env.example .env
# Edite .env e adicione OPENAI_API_KEY

# 4. Execute
python -m src.etl.main --csv SDW2023.csv --mode mock
```

---

## 2. Deploy em Servidor Linux

### Usando systemd (serviço agendado)

```bash
# 1. Clone no servidor
cd /opt
sudo git clone <seu-repo> etl-sdw
cd etl-sdw

# 2. Configure ambiente
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configure .env
sudo nano .env
# Adicione suas variáveis

# 4. Crie arquivo de serviço
sudo nano /etc/systemd/system/etl-sdw.service
```

**Conteúdo do etl-sdw.service**:
```ini
[Unit]
Description=ETL Santander Dev Week
After=network.target

[Service]
Type=oneshot
User=seu-usuario
WorkingDirectory=/opt/etl-sdw
Environment="PATH=/opt/etl-sdw/venv/bin"
ExecStart=/opt/etl-sdw/venv/bin/python -m src.etl.main --csv /opt/etl-sdw/SDW2023.csv --mode real

[Install]
WantedBy=multi-user.target
```

```bash
# 5. Configure timer (execução diária)
sudo nano /etc/systemd/system/etl-sdw.timer
```

**Conteúdo do etl-sdw.timer**:
```ini
[Unit]
Description=ETL Santander Dev Week Timer
Requires=etl-sdw.service

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
# 6. Ative o timer
sudo systemctl daemon-reload
sudo systemctl enable etl-sdw.timer
sudo systemctl start etl-sdw.timer

# 7. Verifique status
sudo systemctl status etl-sdw.timer
sudo systemctl list-timers
```

---

## 3. Deploy com Docker

### Dockerfile

Crie `Dockerfile` na raiz do projeto:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código
COPY src/ ./src/
COPY SDW2023.csv .

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1

# Comando padrão
CMD ["python", "-m", "src.etl.main", "--csv", "SDW2023.csv", "--mode", "mock"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  etl:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SDW_API_URL=${SDW_API_URL}
      - LOG_LEVEL=INFO
    volumes:
      - ./SDW2023.csv:/app/SDW2023.csv
      - ./logs:/app/logs
    command: python -m src.etl.main --csv SDW2023.csv --mode real
```

### Comandos

```bash
# Build
docker build -t etl-sdw .

# Run (modo mock)
docker run --rm etl-sdw

# Run (modo real)
docker run --rm -e OPENAI_API_KEY=sk-... etl-sdw python -m src.etl.main --csv SDW2023.csv --mode real

# Com docker-compose
docker-compose up
```

---

## 4. Deploy na AWS Lambda

### Estrutura

```bash
# 1. Instale dependências em diretório específico
pip install -r requirements.txt -t ./lambda_package

# 2. Copie código
cp -r src lambda_package/

# 3. Crie handler
cat > lambda_package/lambda_handler.py << 'EOF'
import json
import os
from src.etl.main import main as etl_main

def lambda_handler(event, context):
    # Configure variáveis de ambiente
    os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY', '')
    os.environ['SDW_API_URL'] = os.environ.get('SDW_API_URL', '')
    
    # Execute ETL
    try:
        etl_main()
        return {
            'statusCode': 200,
            'body': json.dumps('ETL executado com sucesso')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro: {str(e)}')
        }
EOF

# 4. Crie ZIP
cd lambda_package
zip -r ../etl-lambda.zip .
cd ..
```

### Deploy via AWS CLI

```bash
# Crie função Lambda
aws lambda create-function \
  --function-name etl-sdw \
  --runtime python3.11 \
  --role arn:aws:iam::ACCOUNT_ID:role/lambda-execution-role \
  --handler lambda_handler.lambda_handler \
  --zip-file fileb://etl-lambda.zip \
  --timeout 300 \
  --memory-size 512 \
  --environment Variables="{OPENAI_API_KEY=sk-...,SDW_API_URL=https://...}"

# Configure EventBridge para execução diária
aws events put-rule \
  --name etl-sdw-daily \
  --schedule-expression "cron(0 10 * * ? *)"

aws events put-targets \
  --rule etl-sdw-daily \
  --targets "Id"="1","Arn"="arn:aws:lambda:REGION:ACCOUNT_ID:function:etl-sdw"
```

---

## 5. Deploy no Google Cloud Run

### Dockerfile (otimizado para Cloud Run)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY SDW2023.csv .

ENV PORT=8080
ENV PYTHONUNBUFFERED=1

CMD exec python -m src.etl.main --csv SDW2023.csv --mode real
```

### Deploy

```bash
# 1. Configure projeto
gcloud config set project PROJECT_ID

# 2. Build e push
gcloud builds submit --tag gcr.io/PROJECT_ID/etl-sdw

# 3. Deploy
gcloud run deploy etl-sdw \
  --image gcr.io/PROJECT_ID/etl-sdw \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=sk-...,SDW_API_URL=https://... \
  --no-allow-unauthenticated

# 4. Configure Cloud Scheduler (execução diária)
gcloud scheduler jobs create http etl-sdw-daily \
  --schedule="0 10 * * *" \
  --uri="https://etl-sdw-xxx.run.app" \
  --http-method=POST \
  --oidc-service-account-email=SERVICE_ACCOUNT@PROJECT_ID.iam.gserviceaccount.com
```

---

## 6. Deploy no Heroku

### Procfile

Crie `Procfile` na raiz:

```
worker: python -m src.etl.main --csv SDW2023.csv --mode real
```

### Deploy

```bash
# 1. Login
heroku login

# 2. Crie app
heroku create etl-sdw

# 3. Configure variáveis
heroku config:set OPENAI_API_KEY=sk-...
heroku config:set SDW_API_URL=https://...

# 4. Deploy
git push heroku main

# 5. Configure Scheduler (addon)
heroku addons:create scheduler:standard
heroku addons:open scheduler

# No dashboard, adicione job:
# python -m src.etl.main --csv SDW2023.csv --mode real
# Frequência: Daily
```

---

## 7. Deploy com GitHub Actions (CI/CD)

### Workflow de Deploy Automático

Crie `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 10 * * *'  # Diariamente às 10h UTC

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run ETL
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        SDW_API_URL: ${{ secrets.SDW_API_URL }}
      run: |
        python -m src.etl.main --csv SDW2023.csv --mode real
    
    - name: Notify on failure
      if: failure()
      uses: actions/github-script@v6
      with:
        script: |
          github.rest.issues.create({
            owner: context.repo.owner,
            repo: context.repo.repo,
            title: 'ETL Pipeline Failed',
            body: 'O pipeline ETL falhou. Verifique os logs.'
          })
```

**Configure secrets no GitHub**:
- Settings > Secrets > Actions
- Adicione: `OPENAI_API_KEY`, `SDW_API_URL`

---

## 8. Monitoramento e Logs

### Logs Locais

```bash
# Redirecionar para arquivo
python -m src.etl.main --csv SDW2023.csv --mode real > etl.log 2>&1

# Com rotação de logs (Linux)
python -m src.etl.main --csv SDW2023.csv --mode real | tee -a logs/etl-$(date +%Y%m%d).log
```

### Integração com Sentry

```python
# Adicione ao requirements.txt
sentry-sdk==1.40.0

# Em src/etl/main.py
import sentry_sdk

sentry_sdk.init(
    dsn="https://...@sentry.io/...",
    traces_sample_rate=1.0
)
```

### Integração com CloudWatch (AWS)

```python
# Adicione ao requirements.txt
watchtower==3.0.1

# Em src/etl/utils.py
import watchtower
import logging

logger = logging.getLogger("etl")
logger.addHandler(watchtower.CloudWatchLogHandler())
```

---

## Checklist de Deploy

### Antes do Deploy

- [ ] Testes passando (`pytest`)
- [ ] Lint sem erros (`flake8`)
- [ ] `.env` configurado (não commitar!)
- [ ] CSV de entrada preparado
- [ ] Variáveis de ambiente configuradas
- [ ] Credenciais da OpenAI válidas

### Após o Deploy

- [ ] Executar em modo dry-run primeiro
- [ ] Verificar logs
- [ ] Validar resultados na API
- [ ] Configurar monitoramento
- [ ] Documentar configurações específicas

---

## Troubleshooting de Deploy

### Lambda: Timeout
```bash
# Aumente timeout
aws lambda update-function-configuration \
  --function-name etl-sdw \
  --timeout 900  # 15 minutos
```

### Docker: Imagem muito grande
```dockerfile
# Use imagem slim
FROM python:3.11-slim

# Multi-stage build
FROM python:3.11 as builder
# ... build steps ...
FROM python:3.11-slim
COPY --from=builder /app /app
```

### Heroku: Memória insuficiente
```bash
# Upgrade dyno
heroku ps:scale worker=1:standard-1x
```

---

## Segurança em Produção

1. **Nunca commite secrets**: Use variáveis de ambiente
2. **Rotacione chaves**: Periodicamente
3. **Use HTTPS**: Sempre
4. **Limite permissões**: Princípio do menor privilégio
5. **Monitore logs**: Detecte anomalias
6. **Backup**: Mantenha backups dos dados

---

## Custos Estimados

| Plataforma | Custo Mensal (estimado) |
|------------|-------------------------|
| AWS Lambda | $5-20 (depende de execuções) |
| Google Cloud Run | $5-15 |
| Heroku | $7-25 (dyno básico) |
| Servidor VPS | $5-50 |
| OpenAI API | $10-100 (depende de uso) |

---

## Suporte

Para problemas de deploy, consulte:
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- [README.md](README.md)
- Issues no GitHub
