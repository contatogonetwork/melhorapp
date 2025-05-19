# diagnostico_completo.py
# Execute com: python diagnostico_completo.py

import os
import sys
import importlib
import sqlite3
import pkgutil
from pathlib import Path
from datetime import datetime

def print_header(title):
    print(f"\n{'=' * 50}")
    print(f"{title}".center(50))
    print(f"{'=' * 50}")

def print_section(title):
    print(f"\n{'-' * 50}")
    print(f"[{title}]")
    print(f"{'-' * 50}")

def check_module_imports(module_path):
    try:
        module = importlib.import_module(module_path)
        return "✓", f"{module_path} importado com sucesso"
    except Exception as e:
        return "✗", f"{module_path} falhou: {str(e)}"

def check_ui_modules():
    ui_modules = [
        'gui.main_window',
        'gui.widgets.dashboard_widget',
        'gui.widgets.event_widget',
        'gui.widgets.briefing_widget',
        'gui.widgets.timeline_widget',
        'gui.widgets.assets_widget',
        'gui.widgets.delivery_widget',
        'gui.widgets.settings_widget'
    ]
    
    results = []
    for module in ui_modules:
        status, message = check_module_imports(module)
        results.append((status, message))
    
    return results

def check_data_modules():
    data_modules = [
        'database.Database',
        'database.EventRepository',
        'database.TeamRepository',
        'database.BriefingRepository',
        'database.UserRepository'
    ]
    
    results = []
    for module in data_modules:
        status, message = check_module_imports(module)
        results.append((status, message))
    
    return results

def check_database():
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Verificar tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        table_list = [table[0] for table in tables]
        
        conn.close()
        
        essential_tables = ['events', 'team_members', 'clients', 'users', 'briefings']
        missing_tables = [t for t in essential_tables if t not in table_list]
        
        if missing_tables:
            return "⚠", f"Banco de dados encontrado, mas faltam tabelas: {', '.join(missing_tables)}"
        else:
            return "✓", f"Banco de dados íntegro com {len(table_list)} tabelas"
    except Exception as e:
        return "✗", f"Erro ao acessar banco de dados: {str(e)}"

def check_file_consistency():
    # Verificar se arquivos principais têm importações consistentes
    main_files = {
        'main.py': ['gui.main_window', 'MainWindow'],
        'gui/main_window.py': ['PySide6.QtWidgets', 'gui.widgets']
    }
    
    results = []
    for file_path, expected_imports in main_files.items():
        if not os.path.exists(file_path):
            results.append((f"✗", f"{file_path} não encontrado"))
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        missing_imports = [imp for imp in expected_imports if imp not in content]
        
        if missing_imports:
            results.append((f"⚠", f"{file_path} falta importações: {missing_imports}"))
        else:
            results.append((f"✓", f"{file_path} tem importações consistentes"))
    
    return results

def main():
    print_header("DIAGNÓSTICO COMPLETO DO SISTEMA GONETWORK AI")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Usuário: {os.getlogin()}")
    
    print_section("VERIFICAÇÃO DE MÓDULOS UI")
    ui_results = check_ui_modules()
    for status, message in ui_results:
        print(f"{status} {message}")
    
    print_section("VERIFICAÇÃO DE MÓDULOS DE DADOS")
    data_results = check_data_modules()
    for status, message in data_results:
        print(f"{status} {message}")
    
    print_section("VERIFICAÇÃO DO BANCO DE DADOS")
    db_status, db_message = check_database()
    print(f"{db_status} {db_message}")
    
    print_section("VERIFICAÇÃO DE CONSISTÊNCIA DE ARQUIVOS")
    file_results = check_file_consistency()
    for status, message in file_results:
        print(f"{status} {message}")
    
    print_section("VERIFICAÇÃO DE RECURSOS")
    resources_dir = Path("resources")
    if resources_dir.exists():
        icons_dir = resources_dir / "icons"
        if icons_dir.exists():
            icon_count = len(list(icons_dir.glob("*.svg")))
            print(f"✓ Diretório de ícones encontrado com {icon_count} arquivos SVG")
        else:
            print("⚠ Diretório de ícones não encontrado")
    else:
        print("✗ Diretório de recursos não encontrado")
    
    print_header("DIAGNÓSTICO CONCLUÍDO")
    
    # Calcular resultado geral
    all_results = ui_results + data_results + [(db_status, db_message)] + file_results
    success_count = sum(1 for status, _ in all_results if status == "✓")
    warning_count = sum(1 for status, _ in all_results if status == "⚠")
    error_count = sum(1 for status, _ in all_results if status == "✗")
    
    total_checks = len(all_results)
    success_rate = (success_count / total_checks) * 100
    
    print(f"Taxa de sucesso: {success_rate:.1f}% ({success_count}/{total_checks})")
    print(f"Avisos: {warning_count}, Erros: {error_count}")
    
    if error_count > 0:
        print("\nAÇÕES RECOMENDADAS:")
        print("- Corrija os erros marcados com ✗")
        print("- Execute novamente o diagnóstico após as correções")
    elif warning_count > 0:
        print("\nAÇÕES RECOMENDADAS:")
        print("- Verifique os avisos marcados com ⚠")
        print("- Considere corrigir para melhor estabilidade do sistema")
    else:
        print("\nO SISTEMA PARECE ESTAR EM BOAS CONDIÇÕES!")
    
if __name__ == "__main__":
    main()