"""RAG retriever for entity similarity search"""

from typing import List, Tuple
from langchain_community.vectorstores import Chroma
from ..embeddings.embedder import EntityEmbedder
from ..config import TOP_K_RESULTS, SIMILARITY_THRESHOLD


class EntityRetriever:
    """Retrieves relevant entities based on queries"""
    
    def __init__(self, vectorstore: Chroma = None):
        self.vectorstore = vectorstore
        self.embedder = EntityEmbedder()
    
    def set_vectorstore(self, vectorstore: Chroma) -> None:
        """Set the vector store"""
        self.vectorstore = vectorstore
    
    def retrieve_similar_entities(
        self, 
        query: str, 
        k: int = TOP_K_RESULTS,
        threshold: float = SIMILARITY_THRESHOLD
    ) -> List[Tuple[str, float]]:
        """Retrieve entities similar to query"""
        if self.vectorstore is None:
            raise ValueError("Vectorstore not initialized")
        
        # Use similarity search with scores
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        
        # Filter by threshold
        filtered_results = [
            (doc.metadata.get("entity_id"), 1 - score)  # Convert distance to similarity
            for doc, score in results
            if 1 - score >= threshold
        ]
        
        return filtered_results
    
    def retrieve_by_entity_type(
        self,
        entity_type: str,
        k: int = TOP_K_RESULTS
    ) -> List[str]:
        """Retrieve entities of a specific type"""
        if self.vectorstore is None:
            raise ValueError("Vectorstore not initialized")
        
        docs = self.vectorstore.get_by_metadata({"entity_type": entity_type})
        entity_ids = [doc.metadata.get("entity_id") for doc in docs[:k]]
        
        return entity_ids
    
    def retrieve_connections(
        self,
        source_entity_id: str,
        entity_type: str = None
    ) -> List[Tuple[str, float]]:
        """Retrieve potential connections for an entity"""
        if self.vectorstore is None:
            raise ValueError("Vectorstore not initialized")
        
        # Get the source entity
        docs = self.vectorstore.get_by_metadata({"entity_id": source_entity_id})
        if not docs:
            return []
        
        source_doc = docs[0]
        
        # Find similar entities
        results = self.vectorstore.similarity_search_with_score(
            source_doc.page_content,
            k=TOP_K_RESULTS + 1  # +1 to exclude self
        )
        
        connections = []
        for doc, score in results:
            entity_id = doc.metadata.get("entity_id")
            if entity_id != source_entity_id:  # Exclude self
                if entity_type is None or doc.metadata.get("entity_type") == entity_type:
                    connections.append((entity_id, 1 - score))
        
        return connections
