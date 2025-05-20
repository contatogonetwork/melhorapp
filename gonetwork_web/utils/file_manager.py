import os
import shutil
import mimetypes
import hashlib
from datetime import datetime
import streamlit as st


class FileManager:
    """
    Classe para gerenciar operações com arquivos no sistema.
    """
    
    @staticmethod
    def get_file_uploads_path():
        """Retorna o caminho para o diretório de uploads"""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uploads_path = os.path.join(base_path, "data", "uploads")
        os.makedirs(uploads_path, exist_ok=True)
        return uploads_path
    
    @staticmethod
    def get_thumbnails_path():
        """Retorna o caminho para o diretório de miniaturas"""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        thumbs_path = os.path.join(base_path, "data", "thumbnails")
        os.makedirs(thumbs_path, exist_ok=True)
        return thumbs_path
    
    @staticmethod
    def get_file_info(file_path):
        """
        Obtém informações sobre um arquivo
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            dict: Informações do arquivo
        """
        try:
            # Verificar se o caminho é relativo ao diretório de uploads
            if not os.path.isabs(file_path):
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                abs_file_path = os.path.join(base_path, file_path)
            else:
                abs_file_path = file_path
                
            if not os.path.exists(abs_file_path):
                return None
                
            # Obter informações básicas
            file_stat = os.stat(abs_file_path)
            file_name = os.path.basename(abs_file_path)
            file_ext = os.path.splitext(file_name)[1].lower()
            
            # Determinar o tipo MIME
            mime_type, _ = mimetypes.guess_type(abs_file_path)
            file_type = mime_type.split('/')[0] if mime_type else "unknown"
            
            # Calcular o hash MD5 do arquivo (opcional, pode ser lento para arquivos grandes)
            # md5_hash = FileManager.calculate_file_hash(abs_file_path)
            
            return {
                "name": file_name,
                "path": file_path,  # Caminho relativo para armazenamento
                "abs_path": abs_file_path,  # Caminho absoluto para operações
                "size": file_stat.st_size,
                "modified": datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                "created": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                "extension": file_ext,
                "type": file_type,
                "mime": mime_type,
                # "md5": md5_hash
            }
        except Exception as e:
            st.error(f"Erro ao obter informações do arquivo: {e}")
            return None
    
    @staticmethod
    def calculate_file_hash(file_path, algorithm='md5', buffer_size=65536):
        """
        Calcula o hash de um arquivo
        
        Args:
            file_path: Caminho do arquivo
            algorithm: Algoritmo de hash (md5, sha1, sha256)
            buffer_size: Tamanho do buffer para leitura
            
        Returns:
            str: Hash do arquivo em formato hexadecimal
        """
        try:
            if algorithm == 'md5':
                hash_obj = hashlib.md5()
            elif algorithm == 'sha1':
                hash_obj = hashlib.sha1()
            elif algorithm == 'sha256':
                hash_obj = hashlib.sha256()
            else:
                raise ValueError(f"Algoritmo de hash não suportado: {algorithm}")
                
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(buffer_size)
                    if not data:
                        break
                    hash_obj.update(data)
                    
            return hash_obj.hexdigest()
        except Exception as e:
            st.error(f"Erro ao calcular hash do arquivo: {e}")
            return None
            
    @staticmethod
    def delete_file(file_path):
        """
        Exclui um arquivo do sistema
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            bool: True se o arquivo foi excluído com sucesso
        """
        try:
            # Verificar se o caminho é relativo ao diretório de uploads
            if not os.path.isabs(file_path):
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                abs_file_path = os.path.join(base_path, file_path)
            else:
                abs_file_path = file_path
                
            if os.path.exists(abs_file_path):
                os.remove(abs_file_path)
                return True
            return False
        except Exception as e:
            st.error(f"Erro ao excluir arquivo: {e}")
            return False
    
    @staticmethod
    def list_files(directory_path=None, filter_ext=None):
        """
        Lista arquivos em um diretório
        
        Args:
            directory_path: Caminho do diretório
            filter_ext: Lista de extensões para filtrar (ex: ['.jpg', '.png'])
            
        Returns:
            list: Lista de informações de arquivos
        """
        if directory_path is None:
            directory_path = FileManager.get_file_uploads_path()
            
        try:
            files_list = []
            for file_name in os.listdir(directory_path):
                file_path = os.path.join(directory_path, file_name)
                
                # Pular diretórios
                if os.path.isdir(file_path):
                    continue
                    
                # Aplicar filtro por extensão, se especificado
                if filter_ext and os.path.splitext(file_name)[1].lower() not in filter_ext:
                    continue
                
                # Obter informações do arquivo
                rel_path = os.path.join("data", "uploads", file_name)
                file_info = FileManager.get_file_info(rel_path)
                
                if file_info:
                    files_list.append(file_info)
                    
            return files_list
        except Exception as e:
            st.error(f"Erro ao listar arquivos: {e}")
            return []
