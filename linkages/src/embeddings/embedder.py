"""Entity embedding generation using OpenAI"""

from typing import List
from langchain_openai import OpenAIEmbeddings
from ..config import EMBEDDING_MODEL, OPENAI_API_KEY
from ..data.models import Entity


class EntityEmbedder:
    """Generates embeddings for entities"""
    
    def __init__(self, model: str = EMBEDDING_MODEL, api_key: str = OPENAI_API_KEY):
        self.embedder = OpenAIEmbeddings(
            model=model,
            api_key=api_key
        )
        self.model = model
    
    def embed_entity(self, entity: Entity) -> List[float]:
        """Embed a single entity"""
        text = self._prepare_text(entity)
        return self.embedder.embed_query(text)
    
    def embed_entities(self, entities: List[Entity]) -> List[List[float]]:
        """Embed multiple entities"""
        texts = [self._prepare_text(e) for e in entities]
        return self.embedder.embed_documents(texts)
    
    @staticmethod
    def _prepare_text(entity: Entity) -> str:
        """Prepare entity text for embedding"""
        parts = [
            f"{entity.name}",
            f"Type: {entity.entity_type}",
            f"Description: {entity.description}"
        ]
        
        # Add type-specific information
        if hasattr(entity, 'aum'):
            if entity.aum:
                parts.append(f"AUM: ${entity.aum}M")
            if hasattr(entity, 'headquarters') and entity.headquarters:
                parts.append(f"Headquarters: {entity.headquarters}")
        
        if hasattr(entity, 'size') and entity.size:
            parts.append(f"Size: ${entity.size}M")
        
        if hasattr(entity, 'deal_type') and entity.deal_type:
            parts.append(f"Deal Type: {entity.deal_type}")
        
        if hasattr(entity, 'service_category') and entity.service_category:
            parts.append(f"Service: {entity.service_category}")
        
        return " | ".join(parts)
    
    def embed_query(self, query: str) -> List[float]:
        """Embed a query string"""
        return self.embedder.embed_query(query)
