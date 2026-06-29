"""Vector store indexing for entities"""

from typing import List
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from ..embeddings.embedder import EntityEmbedder
from ..data.models import Entity
from ..config import CHUNK_SIZE, CHUNK_OVERLAP


class EntityIndexer:
    """Indexes entities in vector store"""
    
    def __init__(self, persist_dir: str = "./linkages_vectorstore"):
        self.persist_dir = persist_dir
        self.embedder = EntityEmbedder()
        self.vectorstore = None
    
    def index_entities(self, entities: List[Entity]) -> Chroma:
        """Index entities in vector store"""
        documents = self._prepare_documents(entities)
        
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embedder.embedder,
            persist_directory=self.persist_dir
        )
        
        self.vectorstore.persist()
        return self.vectorstore
    
    def add_entities(self, entities: List[Entity]) -> None:
        """Add entities to existing index"""
        if self.vectorstore is None:
            self.index_entities(entities)
            return
        
        documents = self._prepare_documents(entities)
        self.vectorstore.add_documents(documents)
        self.vectorstore.persist()
    
    def load_vectorstore(self) -> Chroma:
        """Load existing vector store"""
        self.vectorstore = Chroma(
            persist_directory=self.persist_dir,
            embedding_function=self.embedder.embedder
        )
        return self.vectorstore
    
    @staticmethod
    def _prepare_documents(entities: List[Entity]) -> List[Document]:
        """Convert entities to documents"""
        documents = []
        
        for entity in entities:
            content = f"""
Entity ID: {entity.id}
Entity Name: {entity.name}
Entity Type: {entity.entity_type}
Description: {entity.description}

Details:
"""
            # Add type-specific details
            if hasattr(entity, 'aum'):
                if entity.aum:
                    content += f"Assets Under Management: ${entity.aum}M\n"
                if hasattr(entity, 'headquarters') and entity.headquarters:
                    content += f"Headquarters: {entity.headquarters}\n"
            
            if hasattr(entity, 'size') and entity.size:
                content += f"Fund Size: ${entity.size}M\n"
            
            if hasattr(entity, 'deal_type') and entity.deal_type:
                content += f"Deal Type: {entity.deal_type}\n"
            
            if hasattr(entity, 'service_category') and entity.service_category:
                content += f"Service Category: {entity.service_category}\n"
            
            metadata = {
                "entity_id": entity.id,
                "entity_type": entity.entity_type,
                "name": entity.name
            }
            metadata.update(entity.metadata)
            
            doc = Document(page_content=content, metadata=metadata)
            documents.append(doc)
        
        return documents
