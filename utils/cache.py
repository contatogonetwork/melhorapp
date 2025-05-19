"""
Módulo de cache para o sistema GoNetwork AI.

Implementa uma solução de cache em memória para armazenar
dados frequentemente acessados e melhorar a performance do sistema.
"""

import time
from collections import OrderedDict
from typing import Any, Dict, Generic, Optional, Tuple, TypeVar

from utils.logger import get_logger

K = TypeVar("K")  # Tipo da chave
V = TypeVar("V")  # Tipo do valor


class Cache(Generic[K, V]):
    """
    Implementação de cache em memória com expiração de itens.

    Usa OrderedDict para manter a ordem de inserção e remover itens antigos
    quando o limite de tamanho é atingido (política LRU - Least Recently Used).
    """

    def __init__(self, max_size: int = 100, ttl: int = 3600):
        """
        Inicializa o cache com tamanho máximo e tempo de vida (TTL).

        Args:
            max_size: Número máximo de itens no cache
            ttl: Tempo de vida dos itens em segundos
        """
        self._cache: OrderedDict[K, Tuple[V, float]] = OrderedDict()
        self.max_size = max_size
        self.ttl = ttl
        self.logger = get_logger("cache")
        self.hits = 0
        self.misses = 0

    def get(self, key: K) -> Optional[V]:
        """
        Recupera um valor do cache pela chave.

        Args:
            key: Chave para buscar no cache

        Returns:
            O valor associado à chave ou None se não encontrado ou expirado
        """
        if key not in self._cache:
            self.misses += 1
            return None

        value, timestamp = self._cache[key]

        # Verificar se o item expirou
        if time.time() - timestamp > self.ttl:
            # O item expirou, removê-lo
            self._cache.pop(key)
            self.misses += 1
            return None

        # Mover para o final (usado mais recentemente)
        self._cache.move_to_end(key)
        self.hits += 1
        return value

    def set(self, key: K, value: V) -> None:
        """
        Armazena um valor no cache associado a uma chave.

        Se o cache atingir o tamanho máximo, o item menos recentemente
        utilizado será removido.

        Args:
            key: Chave para indexar o valor
            value: Valor a ser armazenado
        """
        # Se já existe, atualizar e mover para o final
        if key in self._cache:
            self._cache.pop(key)

        # Se o cache estiver cheio, remover o item mais antigo
        if len(self._cache) >= self.max_size:
            self._cache.popitem(last=False)

        # Adicionar o novo item com timestamp atual
        self._cache[key] = (value, time.time())

    def invalidate(self, key: K) -> bool:
        """
        Remove um item específico do cache.

        Args:
            key: Chave do item a ser removido

        Returns:
            True se o item foi removido, False se não existia
        """
        if key in self._cache:
            self._cache.pop(key)
            return True
        return False

    def clear(self) -> None:
        """Remove todos os itens do cache."""
        self._cache.clear()
        self.hits = 0
        self.misses = 0

    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas de uso do cache.

        Returns:
            Dicionário com estatísticas como tamanho, hits, misses e taxa de acerto
        """
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0

        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
        }
