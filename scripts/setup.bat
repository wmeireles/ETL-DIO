@echo off
echo ============================================================
echo Setup do Projeto ETL - Santander Dev Week 2023
echo ============================================================
echo.

echo [1/4] Criando ambiente virtual...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERRO: Falha ao criar ambiente virtual
    exit /b 1
)

echo [2/4] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo [3/4] Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias
    exit /b 1
)

echo [4/4] Configurando arquivo .env...
if not exist .env (
    copy .env.example .env
    echo Arquivo .env criado! Edite-o para adicionar sua OPENAI_API_KEY
) else (
    echo Arquivo .env ja existe, pulando...
)

echo.
echo ============================================================
echo Setup concluido com sucesso!
echo ============================================================
echo.
echo Proximos passos:
echo   1. Edite o arquivo .env e adicione sua OPENAI_API_KEY
echo   2. Execute: python -m src.etl.main --csv SDW2023.csv --mode mock
echo.
echo Para ativar o ambiente virtual novamente:
echo   venv\Scripts\activate.bat
echo.
pause
