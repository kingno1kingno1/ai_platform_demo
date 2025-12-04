
from typing import Any, Dict, List

from .base import BaseAgent
from ..rag.vector_store import VectorStore


class ResearchAgent(BaseAgent):
    def __init__(self, vector_store: VectorStore):
        super().__init__(name="research_agent")
        self.vector_store = vector_store

    async def run(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        docs = self.vector_store.search(query, top_k=5)
        context_texts: List[str] = [d.text for d in docs]
        return {
            "retrieved_docs": context_texts,
        }
