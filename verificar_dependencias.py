# verificar_dependencias.py
# Execute com: python verificar_dependencias.py

import os
import sys
import importlib
import pkg_resources

def check_package(package_name):
    """Verifica se um pacote está instalado e sua versão"""
    try:
        package = pkg_resources.get_distribution(package_name)
        return True, f"{package.key} {package.version}"
    except pkg_resources.DistributionNotFound:
        return False, f"{package_name} não encontrado"

def scan_imports_in_file(file_path):
    """Escaneia um arquivo em busca de importações"""
    imports = set()
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                # Remover comentários
                if '#' in line:
                    line = line[:line.index('#')]
                
                # Obter o módulo principal
                if line.startswith('import '):
                    module = line[7:].strip().split(' as ')[0].split(',')[0].strip()
                    imports.add(module.split('.')[0])
                elif line.startswith('from '):
                    module = line[5:].strip().split(' import ')[0]
                    imports.add(module.split('.')[0])
    
    return imports

def main():
    print(f"{'=' * 60}")
    print("VERIFICAÇÃO DE DEPENDÊNCIAS DO PROJETO GONETWORK AI")
    print(f"{'=' * 60}")
    
    # Lista de pacotes essenciais
    essential_packages = [
        'PySide6', 'sqlite3', 'pytest', 'pillow', 'jinja2', 
        'requests', 'datetime', 'uuid'
    ]
    
    print("\nVerificando pacotes essenciais...")
    for package in essential_packages:
        installed, version = check_package(package)
        status = "✓" if installed else "✗"
        print(f"{status} {version}")
    
    print("\nEscaneando arquivos Python para importações...")
    import_count = {}
    file_count = 0
    
    # Escanear todos os arquivos Python do projeto
    for root, _, files in os.walk('.'):
        if '__pycache__' in root or '.venv' in root or 'venv' in root:
            continue
            
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                file_count += 1
                try:
                    file_imports = scan_imports_in_file(file_path)
                    for module in file_imports:
                        import_count[module] = import_count.get(module, 0) + 1
                except Exception as e:
                    print(f"Erro ao escanear {file_path}: {e}")
    
    print(f"\nTotal de {file_count} arquivos Python escaneados.")
    print("\nImportações mais utilizadas:")
    
    # Ordenar por frequência
    sorted_imports = sorted(import_count.items(), key=lambda x: x[1], reverse=True)
    for module, count in sorted_imports[:15]:  # Top 15
        installed, _ = check_package(module)
        status = "✓" if installed or module in sys.builtin_module_names or module in ['database', 'gui', 'resources'] else "?"
        print(f"{status} {module}: {count} arquivos")
    
    print(f"\n{'=' * 60}")
    print("Verificação de Dependências Concluída")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()