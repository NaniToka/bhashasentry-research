from abc import ABC, abstractmethod
from typing import List, Tuple
from bhashasentry.core.types import Query, Passage

class BaseRetriever(ABC):
    """Abstract base interface for multilingual retrievers."""
    
    @abstractmethod
    def index(self, passages: List[Passage]) -> None:
        """Index candidate passages."""
        pass
        
    @abstractmethod
    def retrieve(self, query: Query, top_k: int = 5) -> List[Tuple[Passage, float]]:
        """Retrieve top-k relevant passages with their relevance scores."""
        pass
