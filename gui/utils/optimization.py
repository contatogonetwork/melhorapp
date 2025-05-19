"""
Módulo com funções utilitárias para otimização da interface gráfica.

Este módulo fornece decoradores e funções auxiliares para melhorar
o desempenho e a experiência do usuário na interface gráfica.
"""

from functools import wraps
from typing import Any, Callable, List, TypeVar

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QTableWidget, QWidget

from utils.logger import get_logger

logger = get_logger("gui_utils")

T = TypeVar("T")


def optimize_table_update(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorador para otimizar a atualização de tabelas.

    Desabilita as atualizações da tabela durante a execução da função decorada
    e as reabilita ao final, melhorando a performance em atualizações em lote.

    Args:
        func: Função a ser decorada que atualiza uma tabela

    Returns:
        Função decorada que otimiza as atualizações
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        table = None

        # Identificar o widget de tabela
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, QTableWidget):
                table = attr
                break

        if table:
            # Desabilitar atualizações
            table.setUpdatesEnabled(False)

            try:
                result = func(self, *args, **kwargs)
                return result
            finally:
                # Reabilitar atualizações
                table.setUpdatesEnabled(True)
                table.viewport().update()
        else:
            # Se não encontrou tabela, executa normalmente
            return func(self, *args, **kwargs)

    return wrapper


def batch_update_table(
    table: QTableWidget,
    items: List[Any],
    update_func: Callable[[QTableWidget, Any], None],
) -> None:
    """
    Atualiza uma tabela em lote de forma otimizada.

    Args:
        table: Widget de tabela a ser atualizado
        items: Lista de itens a serem adicionados/atualizados
        update_func: Função que atualiza um item na tabela
    """
    # Desabilitar atualizações
    table.setUpdatesEnabled(False)

    try:
        for item in items:
            update_func(table, item)
    finally:
        # Reabilitar atualizações
        table.setUpdatesEnabled(True)
        table.viewport().update()


def show_busy_cursor(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorador para mostrar cursor de espera durante operações longas.

    Args:
        func: Função a ser decorada

    Returns:
        Função decorada que mostra cursor de espera
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            return func(*args, **kwargs)
        finally:
            QApplication.restoreOverrideCursor()

    return wrapper


def debounce(wait_ms: int = 300) -> Callable:
    """
    Decorador para evitar chamadas repetidas de uma função em curto intervalo.

    Útil para operações como filtragem enquanto o usuário digita.

    Args:
        wait_ms: Tempo de espera em milissegundos

    Returns:
        Decorador configurado com o tempo de espera especificado
    """

    def decorator(func):
        timer = None

        @wraps(func)
        def debounced(*args, **kwargs):
            nonlocal timer
            if timer is not None:
                timer.stop()

            timer = QTimer()
            timer.setSingleShot(True)
            timer.timeout.connect(lambda: func(*args, **kwargs))
            timer.start(wait_ms)

        return debounced

    return decorator
