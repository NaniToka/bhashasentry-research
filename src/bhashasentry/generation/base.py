from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from bhashasentry.core.types import Query, Passage

class BaseGenerator(ABC):
    """Abstract interface for generation engines."""
    
    @abstractmethod
    def generate(self, query: Query, context_passages: List[Passage]) -> str:
        """Generate answer grounded in context passages."""
        pass
