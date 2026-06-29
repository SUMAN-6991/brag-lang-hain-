"""Configuration module for Linkages project"""

import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# Vector Store Configuration
VECTOR_STORE_TYPE = os.getenv("VECTOR_STORE_TYPE", "chromadb")  # chromadb or pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_API_HOST = os.getenv("PINECONE_API_HOST")

# Embedding Configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "1536"))

# Entity Types
ENTITY_TYPES = {
    "firm": "Investment firms and alternative asset managers",
    "fund": "Investment funds and vehicles",
    "deal": "Investment deals and transactions",
    "service_provider": "Service providers and supporting companies"
}

# Relationship Types
RELATIONSHIP_TYPES = {
    "firm_funds": "Firms that manage funds",
    "fund_deals": "Funds that invest in deals",
    "deal_providers": "Service providers working on deals",
    "firm_providers": "Service providers working with firms",
    "fund_providers": "Service providers working with funds"
}

# Chunk Configuration
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# RAG Configuration
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "5"))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))

# Debug mode
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
