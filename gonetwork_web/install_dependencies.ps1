# Script PowerShell para instalar dependências do GoNetwork Web

Write-Host "===== Instalando dependências para GoNetwork Web =====" -ForegroundColor Green

# Verificar se estamos em um ambiente virtual
$inVenv = $env:VIRTUAL_ENV -ne $null
if (-not $inVenv) {
    Write-Host "AVISO: Não foi detectado um ambiente virtual. Recomenda-se criar um." -ForegroundColor Yellow
    Write-Host "Para criar um ambiente virtual, execute:"
    Write-Host "python -m venv venv" -ForegroundColor Cyan
    Write-Host "E depois ative-o com:"
    Write-Host ".\venv\Scripts\Activate" -ForegroundColor Cyan
    Write-Host ""
    $continue = Read-Host "Deseja continuar mesmo assim? (s/n)"
    if ($continue -ne "s") {
        Write-Host "Instalação cancelada." -ForegroundColor Red
        exit 1
    }
}

# Verificar arquitetura do Python
Write-Host "Verificando ambiente Python..." -ForegroundColor Cyan
python -c "import platform; print(f'Arquitetura Python: {platform.architecture()}')"

# Atualizar pip
Write-Host "Atualizando pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# Instalar dependências do requirements.txt
Write-Host "Instalando dependências do requirements.txt..." -ForegroundColor Cyan
pip install -r requirements.txt

# Corrigir problemas com PySide6
Write-Host "Reinstalando PySide6 com suporte completo a multimídia..." -ForegroundColor Cyan
pip uninstall PySide6 PySide6-Addons PySide6-Essentials -y
pip install PySide6==6.6.1 --force-reinstall
pip install PySide6[tools] --upgrade --force-reinstall

# Limpar cache
Write-Host "Limpando cache de pip..." -ForegroundColor Cyan
pip cache purge

# Testar importações
Write-Host "Testando importações do PySide6..." -ForegroundColor Cyan
try {
    python -c "from PySide6.QtMultimedia import QMediaPlayer; print('QtMultimedia: OK')"
    python -c "from PySide6.QtMultimediaWidgets import QVideoWidget; print('QtMultimediaWidgets: OK')"
    Write-Host "Importações PySide6 OK!" -ForegroundColor Green
} catch {
    Write-Host "Aviso: Algumas importações do PySide6 falharam. Isso pode afetar funcionalidades multimídia." -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host "Executando teste completo de importações..." -ForegroundColor Cyan
python utils/test_imports_web.py

Write-Host "===== Instalação concluída! =====" -ForegroundColor Green
