#!/bin/bash
# diagnose_project.sh
# Execute com: bash diagnose_project.sh

echo "======================================================"
echo "   DIAGNÓSTICO COMPLETO - GONETWORK AI"
echo "   $(date)"
echo "   Usuário: $USER"
echo "======================================================"

echo -e "\n[1] VERIFICANDO ESTRUTURA DO PROJETO"
echo "------------------------------------------------------"

# Verifica estrutura de diretórios principal
for dir in database gui resources tests; do
  if [ -d "$dir" ]; then
    echo "✓ Diretório $dir: Encontrado"
  else
    echo "✗ Diretório $dir: Não encontrado"
  fi
done

# Verifica arquivos principais
for file in main.py config.py requirements.txt; do
  if [ -f "$file" ]; then
    echo "✓ Arquivo $file: Encontrado"
  else
    echo "✗ Arquivo $file: Não encontrado"
  fi
done

echo -e "\n[2] VERIFICANDO AMBIENTE PYTHON"
echo "------------------------------------------------------"
python --version
pip --version
echo -e "\nDependências instaladas:"
pip list | grep -E "(PySide6|sqlite|pytest)"

echo -e "\n[3] EXECUTANDO ANÁLISE DE CÓDIGO"
echo "------------------------------------------------------"
echo "Verificando problemas de sintaxe em arquivos Python:"
find . -name "*.py" -exec python -m py_compile {} \; 2>&1 | grep -v "__pycache__" || echo "✓ Nenhum erro de sintaxe encontrado"

echo -e "\n[4] VERIFICANDO BANCO DE DADOS"
echo "------------------------------------------------------"
if [ -f "database.db" ]; then
  echo "✓ Arquivo de banco de dados encontrado"
  echo "Tabelas no banco de dados:"
  sqlite3 database.db ".tables" 2>/dev/null || echo "✗ Erro ao acessar o banco de dados"
else
  echo "✗ Arquivo de banco de dados não encontrado"
fi

echo -e "\n[5] TESTE DE INICIALIZAÇÃO DO APLICATIVO"
echo "------------------------------------------------------"
echo "Tentando inicializar o aplicativo (timeout de 5 segundos):"
timeout 5s python main.py 2>&1 || echo "Timeout atingido (comportamento esperado)"

echo "======================================================"
echo "           DIAGNÓSTICO CONCLUÍDO"
echo "======================================================"