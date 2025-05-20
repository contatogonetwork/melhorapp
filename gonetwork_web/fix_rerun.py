"""
Script para substituir todas as ocorrências de st.rerun() por st.rerun()
"""

import glob
import os
import re


def replace_experimental_rerun():
    # Diretório raiz
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # Padrão a ser substituído e sua substituição
    pattern = r"st\.experimental_rerun\(\)"
    replacement = "st.rerun()"

    # Encontrar todos os arquivos Python
    py_files = glob.glob(os.path.join(root_dir, "**/*.py"), recursive=True)

    # Contador de arquivos e substituições
    files_modified = 0
    replacements_made = 0

    print(f"[ℹ️] Encontrados {len(py_files)} arquivos Python")

    # Percorrer cada arquivo e fazer as substituições
    for file_path in py_files:
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                content = file.read()
            except UnicodeDecodeError:
                print(f"   - Erro ao ler {file_path} (problema de codificação)")
                continue

        # Verificar se o padrão está presente
        if re.search(pattern, content):
            # Fazer a substituição
            new_content = re.sub(pattern, replacement, content)

            # Contar substituições
            count = len(re.findall(pattern, content))
            replacements_made += count

            # Salvar o arquivo modificado
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(new_content)

            files_modified += 1
            print(f"   - Modificado {file_path} ({count} substituições)")

    print(
        f"[✅] Processo concluído: {files_modified} arquivos modificados, {replacements_made} substituições feitas"
    )


if __name__ == "__main__":
    replace_experimental_rerun()
