# 🏗️ Arquitetura do Projeto

## Visão Geral

Este projeto implementa um pipeline ETL (Extract, Transform, Load) seguindo princípios de Clean Architecture e SOLID.

## Diagrama de Fluxo

```
┌─────────────┐
│ SDW2023.csv │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│                    EXTRACT PHASE                        │
│  ┌──────────────┐         ┌──────────────────────┐     │
│  │  read_csv()  │────────▶│  extract_users()     │     │
│  └──────────────┘         │  - get_user() x N    │     │
│                           │  - Retry logic       │     │
│                           │  - Error handling    │     │
│                           └──────────┬───────────┘     │
└────────────────────────────────────────┼───────────────┘
                                         │
                                         ▼
                                  [User Objects]
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────┐
│                   TRANSFORM PHASE                       │
│  ┌──────────────────────────────────────────────┐      │
│  │  transform_users()                           │      │
│  │    ├─ generate_message()                     │      │
│  │    │   ├─ Mode: Real → OpenAI GPT-4          │      │
│  │    │   │   - Retry with backoff               │      │
│  │    │   │   - Timeout handling                 │      │
│  │    │   │   - Fallback to mock                 │      │
│  │    │   └─ Mode: Mock → Local generation       │      │
│  │    └─ truncate_message() (max 100 chars)     │      │
│  └──────────────────────┬───────────────────────┘      │
└─────────────────────────┼───────────────────────────────┘
                          │
                          ▼
                   [User Objects + Messages]
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                     LOAD PHASE                          │
│  ┌──────────────────────────────────────────────┐      │
│  │  load_users()                                │      │
│  │    ├─ add_news_to_user()                     │      │
│  │    │   └─ is_duplicate_news() (idempotency)  │      │
│  │    └─ update_user()                          │      │
│  │        - PUT /users/{id}                     │      │
│  │        - Retry with backoff                  │      │
│  │        - Dry run support                     │      │
│  └──────────────────────┬───────────────────────┘      │
└─────────────────────────┼───────────────────────────────┘
                          │
                          ▼
                    [Updated Users]
                          │
                          ▼
                   ┌──────────────┐
                   │   Statistics │
                   │  - Success   │
                   │  - Failed    │
                   │  - Skipped   │
                   └──────────────┘
```

## Componentes Principais

### 1. Extract (extract.py)
**Responsabilidade**: Extração de dados de fontes externas

**Funções**:
- `read_csv(file_path)`: Lê IDs do CSV usando pandas
- `get_user(user_id)`: Busca dados de um usuário via API REST
- `extract_users(user_ids)`: Orquestra extração de múltiplos usuários

**Características**:
- Retry automático com backoff exponencial
- Timeout configurável (10s)
- Tratamento de erros HTTP (404, 500, etc.)
- Logging detalhado

### 2. Transform (transform.py)
**Responsabilidade**: Transformação de dados e geração de conteúdo

**Funções**:
- `generate_message_openai(user)`: Gera mensagem via OpenAI GPT-4
- `generate_message_mock(user)`: Gera mensagem local (sem API)
- `generate_message(user, mode)`: Abstração que escolhe o método
- `transform_users(users, mode)`: Processa lista de usuários

**Características**:
- Suporte a modo real (OpenAI) e mock (local)
- Fallback automático para mock em caso de erro
- Truncamento inteligente de mensagens (100 chars)
- Personalização com nome do usuário
- Timeout configurável para OpenAI (30s)

### 3. Load (load.py)
**Responsabilidade**: Carregamento e persistência de dados

**Funções**:
- `is_duplicate_news(user, description)`: Verifica duplicatas
- `add_news_to_user(user, message)`: Adiciona notícia ao usuário
- `update_user(user)`: Atualiza usuário via PUT
- `load_users(users)`: Processa lista de usuários

**Características**:
- Idempotência (não duplica notícias)
- Dry run mode (não faz atualizações reais)
- Retry com backoff exponencial
- Estatísticas de sucesso/falha

### 4. Config (config.py)
**Responsabilidade**: Configurações centralizadas

**Conteúdo**:
- Variáveis de ambiente (.env)
- Timeouts e retries
- URLs e endpoints
- Prompts do OpenAI

### 5. Utils (utils.py)
**Responsabilidade**: Funções auxiliares reutilizáveis

**Funções**:
- `setup_logging()`: Configura sistema de logs
- `retry_with_backoff()`: Decorator para retry automático
- `truncate_message()`: Trunca texto sem cortar palavras

### 6. Main (main.py)
**Responsabilidade**: Orquestração e CLI

**Características**:
- Argumentos de linha de comando (argparse)
- Orquestração do pipeline ETL
- Tratamento de erros global
- Estatísticas finais

## Padrões de Design Utilizados

### 1. Separation of Concerns
Cada módulo tem uma responsabilidade única e bem definida.

### 2. Dependency Injection
Configurações e URLs são injetadas via parâmetros, facilitando testes.

### 3. Decorator Pattern
`@retry_with_backoff` adiciona comportamento de retry sem modificar funções.

### 4. Strategy Pattern
`generate_message()` escolhe estratégia (real/mock) em runtime.

### 5. Fail-Safe / Fallback
Fallback automático para modo mock quando OpenAI falha.

## Tratamento de Erros

### Níveis de Tratamento

1. **Função Individual**: Try/catch local com log
2. **Retry Automático**: Decorator com backoff exponencial
3. **Fallback**: Modo mock quando real falha
4. **Pipeline**: Continua processando outros usuários se um falhar
5. **Global**: Main captura erros fatais e retorna exit code

### Estratégia de Retry

```python
Tentativa 1: Imediato
Tentativa 2: Aguarda 2^0 = 1 segundo
Tentativa 3: Aguarda 2^1 = 2 segundos
Tentativa 4: Aguarda 2^2 = 4 segundos (se MAX_RETRIES > 3)
```

## Idempotência

### Implementação
Antes de adicionar uma notícia, verifica se já existe uma com a mesma descrição:

```python
def is_duplicate_news(user, description):
    for news in user.get('news', []):
        if news.get('description') == description:
            return True
    return False
```

### Limitações
- Compara apenas a descrição exata
- Não considera variações de texto
- Não persiste estado entre execuções

## Segurança

### Boas Práticas Implementadas

1. **Secrets Management**: Chaves em .env (não commitadas)
2. **Timeout**: Todas as requisições têm timeout
3. **Input Validation**: Validação de IDs e dados
4. **Error Handling**: Não expõe stack traces sensíveis
5. **Logging**: Não loga dados sensíveis (tokens, senhas)

## Performance

### Otimizações

1. **Processamento Sequencial**: Simples e confiável
2. **Retry Inteligente**: Backoff exponencial evita sobrecarga
3. **Timeout Configurável**: Evita travamentos
4. **Logging Eficiente**: Níveis configuráveis

### Limitações Conhecidas

1. **Sem Paralelização**: Processa usuários sequencialmente
2. **Sem Cache**: Cada execução busca dados novamente
3. **Sem Persistência**: Não salva estado intermediário

## Extensibilidade

### Pontos de Extensão

1. **Novos Modos**: Adicionar além de real/mock
2. **Novos Transformers**: Diferentes tipos de mensagens
3. **Novos Loaders**: Outros destinos além da API
4. **Middlewares**: Adicionar validações/transformações

### Como Estender

```python
# Exemplo: Adicionar modo "template"
def generate_message_template(user, template):
    return template.format(name=user['name'])

# Em transform.py
if mode == "template":
    return generate_message_template(user, custom_template)
```

## Testes

### Estratégia de Testes

1. **Unitários**: Cada função isoladamente (mocks)
2. **Integração**: Pipeline completo em modo mock
3. **E2E**: Com mock server local

### Cobertura Alvo
- Mínimo: 80%
- Ideal: 90%+

## Monitoramento e Observabilidade

### Logs
- Níveis: DEBUG, INFO, WARNING, ERROR
- Formato: Timestamp + Logger + Level + Message
- Destino: Console (pode ser estendido para arquivo/Syslog)

### Métricas Disponíveis
- Total de usuários processados
- Sucessos / Falhas / Pulados
- Tempo de execução (via logs)

## Deployment

### Ambientes Sugeridos

1. **Local**: Desenvolvimento e testes
2. **CI/CD**: GitHub Actions (já configurado)
3. **Produção**: AWS Lambda, Cloud Run, ou servidor

### Variáveis de Ambiente por Ambiente

**Desenvolvimento**:
```
OPENAI_API_KEY=sk-test-...
SDW_API_URL=http://localhost:5000
LOG_LEVEL=DEBUG
```

**Produção**:
```
OPENAI_API_KEY=sk-prod-...
SDW_API_URL=https://sdw-2023-prd.up.railway.app
LOG_LEVEL=INFO
```

## Roadmap de Melhorias

### Curto Prazo
- [ ] Adicionar cache de usuários
- [ ] Paralelizar requisições (asyncio)
- [ ] Métricas com Prometheus

### Médio Prazo
- [ ] Dashboard de monitoramento
- [ ] Fila de processamento (Celery)
- [ ] Banco de dados para histórico

### Longo Prazo
- [ ] A/B testing de mensagens
- [ ] ML para personalização avançada
- [ ] Multi-tenancy
