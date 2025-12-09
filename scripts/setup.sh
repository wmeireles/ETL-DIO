#!/bin/bash

echo "============================================================"
echo "Setup do Projeto ETL - Santander Dev Week 2023"
echo "============================================================"
echo ""

echo "[1/4] Criando ambiente virtual..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao criar ambiente virtual"
    exit 1
fi

echo "[2/4] Ativando ambiente virtual..."
source venv/bin/activate

echo "[3/4] Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao instalar dependências"
    exit 1
fi

echo "[4/4] Configurando arquivo .env..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Arquivo .env criado! Edite-o para adicionar sua OPENAI_API_KEY"
else
    echo "Arquivo .env já existe, pulando..."
fi

echo ""
echo "============================================================"
echo "Setup concluído com sucesso!"
echo "============================================================"
echo ""
echo "Próximos passos:"
echo "  1. Edite o arquivo .env e adicione sua OPENAI_API_KEY"
echo "  2. Execute: python -m src.etl.main --csv SDW2023.csv --mode mock"
echo ""
echo "Para ativar o ambiente virtual novamente:"
echo "  source venv/bin/activate"
echo ""
