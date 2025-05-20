@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo 🌐 Iniciando GoNetwork Web
echo =============================================

:: Verificar o banco de dados
set "dbPath=c:\melhor\data\gonetwork.db"
if exist "%dbPath%" (
    echo ✅ Banco de dados encontrado
) else (
    echo ❌ Banco de dados não encontrado, configurando...
    python setup_db.py
)

:: Verificar dados de exemplo
python -c "import sqlite3; conn = sqlite3.connect('c:\\melhor\\data\\gonetwork.db'); c = conn.cursor(); c.execute('SELECT COUNT(*) FROM briefings'); print(c.fetchone()[0] > 0)" > temp.txt
set /p hasData=<temp.txt
del temp.txt

if "!hasData!"=="True" (
    echo ✅ Dados de exemplo encontrados
) else (
    echo ❌ Dados de exemplo não encontrados, gerando...
    python fix_db_data.py
)

:: Iniciar a aplicação
echo.
echo 🚀 Iniciando a aplicação GoNetwork Web...
echo Acesse a aplicação em: http://localhost:8501
echo Pressione Ctrl+C para encerrar a aplicação
echo.

streamlit run app.py
