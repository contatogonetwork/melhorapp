# Arquivo para iniciar a aplicação web GoNetwork
$env:PYTHONIOENCODING = "utf-8"

Write-Host "🌐 Iniciando GoNetwork Web" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Verificar o banco de dados
$dbPath = "c:\melhor\data\gonetwork.db"
if (Test-Path $dbPath) {
    Write-Host "✅ Banco de dados encontrado" -ForegroundColor Green
} else {
    Write-Host "❌ Banco de dados não encontrado, configurando..." -ForegroundColor Yellow
    python setup_db.py
}

# Verificar dados de exemplo
$hasData = python -c "import sqlite3; conn = sqlite3.connect('c:\\melhor\\data\\gonetwork.db'); c = conn.cursor(); c.execute('SELECT COUNT(*) FROM briefings'); print(c.fetchone()[0] > 0)"
if ($hasData -eq "True") {
    Write-Host "✅ Dados de exemplo encontrados" -ForegroundColor Green
} else {
    Write-Host "❌ Dados de exemplo não encontrados, gerando..." -ForegroundColor Yellow
    python fix_db_data.py
}

# Iniciar a aplicação
Write-Host "`n🚀 Iniciando a aplicação GoNetwork Web..." -ForegroundColor Cyan
Write-Host "Acesse a aplicação em: http://localhost:8501" -ForegroundColor Green
Write-Host "Pressione Ctrl+C para encerrar a aplicação`n" -ForegroundColor Yellow

streamlit run app.py
