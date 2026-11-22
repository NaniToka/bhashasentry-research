from typing import Dict, Any, Optional

class RetrievalClaimCache:
    """
    In-memory LRU cache storing indexed passage embeddings and verified atomic claims.
    """
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._cache: Dict[str, Any] = {}
        
    def get(self, key: str) -> Optional[Any]:
        return self._cache.get(key)
        
    def put(self, key: str, val: Any) -> None:
        if len(self._cache) >= self.max_size:
            self._cache.pop(next(iter(self._cache)))
        self._cache[key] = val
