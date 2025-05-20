# Script para instalar todas as dependências necessárias para a versão web

echo "===== Instalando dependências para GoNetwork Web ====="

# Ative seu ambiente virtual primeiro (se estiver usando)
# No Windows: venv\Scripts\activate
# No Linux/Mac: source venv/bin/activate

echo "Verificando ambiente Python..."
python -c "import platform; print(f'Arquitetura Python: {platform.architecture()}')"

# Atualizar pip
echo "Atualizando pip..."
pip install --upgrade pip

# Instalar dependências gerais do requirements.txt
echo "Instalando dependências principais..."
pip install -r requirements.txt

# Instalar PySide6 com suporte completo a multimídia
echo "Instalando suporte a multimídia para PySide6..."
pip uninstall PySide6 PySide6-Addons PySide6-Essentials -y
pip install PySide6==6.6.1 --force-reinstall
pip install PySide6[tools] --upgrade --force-reinstall

# Limpar cache de pip
echo "Limpando cache..."
pip cache purge

# Testar importações críticas
echo "Testando importações PySide6..."
python -c "from PySide6.QtMultimedia import QMediaPlayer; print('QtMultimedia: OK')"
python -c "from PySide6.QtMultimediaWidgets import QVideoWidget; print('QtMultimediaWidgets: OK')"

echo "===== Instalação concluída! ====="
echo "Execute 'python utils/test_imports_web.py' para verificar todas as importações"
