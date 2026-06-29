# Linkages - Entity Connection Discovery System

A powerful RAG (Retrieval-Augmented Generation) and LLM-based system for discovering and mapping connections between entities in alternative markets.

## Overview

Linkages helps you understand and visualize the complex web of connections between:
- **Firms** - Investment firms and asset managers
- **Funds** - Investment vehicles and portfolios
- **Deals** - Transactions and investments
- **Service Providers** - Legal, advisory, and support firms

## Key Features

✨ **Connection Discovery**
- Automatically discover connections between entities using similarity search
- LLM-powered reasoning for intelligent connection identification
- Confidence scoring for each connection

📊 **Network Mapping**
- Visualize complex networks of relationships
- Find shortest paths between entities
- Explore entity neighborhoods at various depths

🔍 **RAG Integration**
- Vector-based similarity search for fast retrieval
- Semantic understanding of entity relationships
- Scalable to thousands of entities

🤖 **LLM-Powered Reasoning**
- GPT-4 based connection analysis
- Relationship type classification
- Explanation generation for discovered connections

## Project Structure

```
linkages/
├── src/
│   ├── __init__.py
│   ├── config.py                 # Configuration management
│   ├── data/
│   │   ├── __init__.py
│   │   ├── models.py             # Pydantic entity models
│   │   └── loader.py             # Data ingestion
│   ├── embeddings/
│   │   ├── __init__.py
│   │   └── embedder.py           # Embedding generation
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── indexer.py            # Vector store indexing
│   │   └── retriever.py          # Similarity search
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── connector.py          # LLM reasoning
│   │   └── prompts.py            # Prompt templates
│   └── graph/
│       ├── __init__.py
│       └── linkage_mapper.py     # Connection mapping
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_rag_setup.ipynb
│   ├── 03_linkage_discovery.ipynb
│   └── 04_full_pipeline.ipynb
├── data/
│   ├── sample_firms.csv
│   ├── sample_funds.csv
│   ├── sample_deals.csv
│   └── sample_providers.csv
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites
- Python 3.11+
- OpenAI API key (for LLM and embeddings)
- Optional: Pinecone API key (for cloud vector store)

### Setup

1. **Navigate to linkages directory:**
```bash
cd linkages
```

2. **Create virtual environment:**
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Quick Start

### Load Data and Build Index

```python
from src.data import DataLoader
from src.embeddings import EntityEmbedder
from src.rag import EntityIndexer

# Load entities
loader = DataLoader()
firms = loader.load_csv("sample_firms.csv", "firm")
funds = loader.load_csv("sample_funds.csv", "fund")
deals = loader.load_csv("sample_deals.csv", "deal")
providers = loader.load_csv("sample_providers.csv", "service_provider")

# Index entities
indexer = EntityIndexer()
vectorstore = indexer.index_entities(
    firms + funds + deals + providers
)
```

### Discover Connections

```python
from src.rag import EntityRetriever
from src.llm import ConnectionReasoner
from src.graph import LinkageMapper

# Initialize components
retriever = EntityRetriever(vectorstore)
reasoner = ConnectionReasoner()
mapper = LinkageMapper(retriever, reasoner)

# Discover network connections
all_entities = {e.id: e for e in firms + funds + deals + providers}
connections = mapper.discover_full_network(all_entities, use_llm_reasoning=True)

print(f"Found {len(connections)} connections")
```

### Find Connection Paths

```python
# Find shortest path between entities
source_firm = firms[0]
target_provider = providers[0]

path = mapper.find_shortest_path(
    source_firm,
    target_provider,
    connections
)

if path:
    print(f"Found path with {len(path)} connections")
    for conn in path:
        print(f"  {conn.source_id} -> {conn.target_id}")
```

### Analyze Network Statistics

```python
# Get connection statistics
stats = mapper.get_connection_statistics(connections)
print(f"Total connections: {stats['total_connections']}")
print(f"Entities connected: {stats['entities_connected']}")
print(f"Average connection strength: {stats['average_strength']:.2f}")
print(f"Connections by type: {stats['connections_by_type']}")
```

## Entity Types & Relationships

### Entity Types
- **Firm**: Investment firms and alternative asset managers
- **Fund**: Investment funds and vehicles
- **Deal**: Investment deals and transactions
- **Service Provider**: Service providers and supporting companies

### Relationship Types
- **firm_funds**: Firms that manage funds
- **fund_deals**: Funds that invest in deals
- **deal_providers**: Service providers working on deals
- **firm_providers**: Service providers working with firms
- **fund_providers**: Service providers working with funds

## Configuration

Key configuration options in `.env`:

```env
# LLM Model (gpt-4 recommended for best results)
LLM_MODEL=gpt-4
TEMPERATURE=0.7

# Vector Store
VECTOR_STORE_TYPE=chromadb  # or pinecone

# RAG Parameters
TOP_K_RESULTS=5
SIMILARITY_THRESHOLD=0.5
```

## Notebooks

### 01_data_exploration.ipynb
Explore sample data and understand entity structure

### 02_rag_setup.ipynb
Set up RAG pipeline with embeddings and vector store

### 03_linkage_discovery.ipynb
Discover connections using retriever and LLM reasoning

### 04_full_pipeline.ipynb
Complete end-to-end pipeline with visualization

## API Methods

### EntityRetriever
- `retrieve_similar_entities(query, k)` - Find similar entities
- `retrieve_by_entity_type(entity_type, k)` - Get entities by type
- `retrieve_connections(entity_id, entity_type)` - Find potential connections

### LinkageMapper
- `map_entity_connections(entity)` - Map connections for single entity
- `discover_full_network(entities)` - Discover all connections
- `find_shortest_path(source, target, connections)` - Find connection path
- `get_entity_neighborhood(entity, connections, depth)` - Get connected entities
- `get_connection_statistics(connections)` - Analyze network stats

### ConnectionReasoner
- `find_connection(source, target, context)` - Determine if connection exists
- `explain_connection(connection, source, target)` - Explain a connection
- `discover_linkages(entity, context)` - Discover all linkages
- `find_connection_path(start, end)` - Find path between entities

## Data Format

### Firms CSV
```csv
id,name,description,aum,founded_year,headquarters
firm_001,Example Firm,Description,684000,1985,New York
```

### Funds CSV
```csv
id,name,description,size,fund_type,vintage_year,managing_firm_id
fund_001,Example Fund,Description,50000,Infrastructure,2021,firm_001
```

### Deals CSV
```csv
id,name,description,deal_type,deal_value,target_company,investing_fund_id
deal_001,Example Deal,Description,Investment,5000,Target Corp,fund_001
```

### Service Providers CSV
```csv
id,name,description,service_category,specialization,service_areas
provider_001,Example Provider,Description,Legal,M&A,Legal Services
```

## Extending Linkages

### Add Custom Entity Type
1. Create class in `src/data/models.py` extending `Entity`
2. Add loader logic in `src/data/loader.py`
3. Add valid connections in `LinkageMapper.VALID_CONNECTIONS`

### Use Different LLM
1. Modify `src/llm/connector.py` to use different LLM
2. Update prompts in `src/llm/prompts.py` as needed

### Use Different Vector Store
1. Modify `src/rag/indexer.py` for your store
2. Update `src/rag/retriever.py` accordingly

## Performance Tips

1. **Use Pinecone for large datasets** - Better scalability than ChromaDB
2. **Cache embeddings** - Save computed embeddings for reuse
3. **Batch LLM calls** - Process multiple connections in parallel
4. **Adjust TOP_K_RESULTS** - Lower for faster retrieval, higher for recall

## Troubleshooting

### "No API key provided"
- Ensure `.env` file exists and has `OPENAI_API_KEY` set

### "Vector store not initialized"
- Call `indexer.index_entities()` before using retriever

### Slow connection discovery
- Reduce `TOP_K_RESULTS` in config
- Use retriever-based scoring instead of LLM reasoning
- Consider using Pinecone for faster indexing

## Contributing

Contributions are welcome! Areas for enhancement:
- Visualization modules for connection graphs
- REST API for linkage queries
- Advanced path finding algorithms
- Integration with other data sources

## License

MIT License

## Contact

For questions or suggestions, open an issue or contact the development team.

---

**Built with RAG and LLM to discover the hidden connections in alternative markets.**
