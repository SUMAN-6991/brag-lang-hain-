# Linkages Usage Guide

Complete guide to using the Linkages entity connection discovery system.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Loading Data](#loading-data)
3. [Setting Up RAG](#setting-up-rag)
4. [Discovering Connections](#discovering-connections)
5. [Analyzing Networks](#analyzing-networks)
6. [Advanced Usage](#advanced-usage)

## Quick Start

### 1. Installation

```bash
cd linkages
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

### 2. Basic Usage

```python
from src.data import DataLoader
from src.embeddings import EntityEmbedder
from src.rag import EntityIndexer, EntityRetriever
from src.llm import ConnectionReasoner
from src.graph import LinkageMapper

# Load data
loader = DataLoader()
firms = loader.load_csv('data/sample_firms.csv', 'firm')
funds = loader.load_csv('data/sample_funds.csv', 'fund')
deals = loader.load_csv('data/sample_deals.csv', 'deal')
providers = loader.load_csv('data/sample_providers.csv', 'service_provider')

# Build RAG
all_entities = firms + funds + deals + providers
indexer = EntityIndexer()
vectorstore = indexer.index_entities(all_entities)

# Discover connections
retriever = EntityRetriever(vectorstore)
reasoner = ConnectionReasoner()
mapper = LinkageMapper(retriever, reasoner)

entities_dict = {e.id: e for e in all_entities}
connections = mapper.discover_full_network(entities_dict)

print(f"Found {len(connections)} connections")
```

## Loading Data

### CSV Format

**Firms:**
```csv
id,name,description,aum,founded_year,headquarters
firm_001,Company Name,Description,Amount in Millions,Year,City
```

**Funds:**
```csv
id,name,description,size,fund_type,vintage_year,managing_firm_id
fund_001,Fund Name,Description,Size in Millions,Type,Year,firm_id
```

**Deals:**
```csv
id,name,description,deal_type,deal_value,target_company,investing_fund_id
deal_001,Deal Name,Description,Type,Value in Millions,Target,fund_id
```

**Service Providers:**
```csv
id,name,description,service_category,specialization,service_areas
provider_001,Company Name,Description,Category,Specialization,Areas
```

### Loading Data in Code

```python
from src.data import DataLoader
from pathlib import Path

# Initialize loader
loader = DataLoader(data_dir=Path('data'))

# Load entities
firms = loader.load_csv('firms.csv', 'firm')
funds = loader.load_csv('funds.csv', 'fund')
deals = loader.load_csv('deals.csv', 'deal')
providers = loader.load_csv('providers.csv', 'service_provider')

# Access entities
for firm in firms:
    print(f"{firm.name}: ${firm.aum}M AUM")

# Get all entities
all_entities = loader.get_all_entities()
```

## Setting Up RAG

### 1. Create Embeddings

```python
from src.embeddings import EntityEmbedder

# Initialize embedder
embedder = EntityEmbedder(model='text-embedding-3-small')

# Embed single entity
embedding = embedder.embed_entity(firms[0])

# Embed multiple entities
embeddings = embedder.embed_entities(all_entities)

# Embed query
query_embedding = embedder.embed_query('Looking for infrastructure funds')
```

### 2. Index Entities

```python
from src.rag import EntityIndexer

# Create indexer
indexer = EntityIndexer(persist_dir='./vectorstore')

# Index entities
vectorstore = indexer.index_entities(all_entities)

# Add more entities later
new_entities = [...]
indexer.add_entities(new_entities)

# Load existing index
vectorstore = indexer.load_vectorstore()
```

### 3. Retrieve Similar Entities

```python
from src.rag import EntityRetriever

# Create retriever
retriever = EntityRetriever(vectorstore)

# Find similar entities to query
results = retriever.retrieve_similar_entities(
    query='Leading infrastructure investment',
    k=5,
    threshold=0.5
)
# Returns: [(entity_id, similarity_score), ...]

# Get entities by type
infra_funds = retriever.retrieve_by_entity_type('fund', k=10)

# Find connections for an entity
connections = retriever.retrieve_connections(
    source_entity_id='firm_001',
    entity_type='fund'
)
```

## Discovering Connections

### 1. Using LLM Reasoning

```python
from src.llm import ConnectionReasoner

# Initialize reasoner
reasoner = ConnectionReasoner(model='gpt-4')

# Find connection between two entities
result = reasoner.find_connection(
    source_entity=firms[0],
    target_entity=funds[0],
    context='Alternative markets context'
)

print(f"Connected: {result['is_connected']}")
print(f"Strength: {result['strength']}")
print(f"Evidence: {result['evidence']}")
```

### 2. Discover Full Network

```python
from src.graph import LinkageMapper

# Create mapper
mapper = LinkageMapper(retriever, reasoner)

# Discover all connections
entities_dict = {e.id: e for e in all_entities}
connections = mapper.discover_full_network(
    entities=entities_dict,
    use_llm_reasoning=True  # Set False for faster, retriever-only mode
)

print(f"Found {len(connections)} connections")

# Get statistics
stats = mapper.get_connection_statistics(connections)
print(stats)
```

### 3. Find Connection Paths

```python
# Find shortest path between entities
path = mapper.find_shortest_path(
    source_entity=firms[0],
    target_entity=providers[0],
    connections=connections,
    max_depth=5
)

if path:
    print(f"Path found with {len(path)} steps:")
    for i, conn in enumerate(path):
        print(f"  Step {i+1}: {conn.source_id} -> {conn.target_id}")
```

### 4. Explore Entity Neighborhood

```python
# Get all entities connected at different depths
neighborhood = mapper.get_entity_neighborhood(
    entity=firms[0],
    connections=connections,
    depth=2
)

print(f"Direct connections: {len(neighborhood[1])}")
print(f"Secondary connections: {len(neighborhood[2])}")
```

## Analyzing Networks

### Connection Statistics

```python
# Get comprehensive statistics
stats = mapper.get_connection_statistics(connections)

print(f"Total connections: {stats['total_connections']}")
print(f"Entities connected: {stats['entities_connected']}")
print(f"Average strength: {stats['average_strength']:.2f}")

# By connection type
for conn_type, count in stats['connections_by_type'].items():
    print(f"  {conn_type}: {count}")
```

### Analyze Entity Centrality

```python
# Count connections per entity
entity_connections = {}
for conn in connections:
    entity_connections[conn.source_id] = entity_connections.get(conn.source_id, 0) + 1
    entity_connections[conn.target_id] = entity_connections.get(conn.target_id, 0) + 1

# Find most connected entities
most_connected = sorted(
    entity_connections.items(),
    key=lambda x: x[1],
    reverse=True
)

print("Most connected entities:")
for entity_id, conn_count in most_connected[:5]:
    entity = entities_dict[entity_id]
    print(f"  {entity.name}: {conn_count} connections")
```

### Analyze Connection Strength

```python
# Get connection strength statistics
strengths = [c.strength for c in connections]
avg_strength = sum(strengths) / len(strengths) if strengths else 0
max_strength = max(strengths) if strengths else 0
min_strength = min(strengths) if strengths else 0

print(f"Strength statistics:")
print(f"  Average: {avg_strength:.2f}")
print(f"  Max: {max_strength:.2f}")
print(f"  Min: {min_strength:.2f}")

# Find high-confidence connections
high_confidence = [c for c in connections if c.strength > 0.8]
print(f"High-confidence connections (>0.8): {len(high_confidence)}")
```

## Advanced Usage

### 1. Custom Entity Types

```python
from src.data.models import Entity

# Create custom entity
class HedgeFund(Entity):
    strategy: str
    aum: float
    
    def __init__(self, **data):
        if "entity_type" not in data:
            data["entity_type"] = "hedge_fund"
        super().__init__(**data)
```

### 2. Batch Processing

```python
# Process many connections efficiently
from concurrent.futures import ThreadPoolExecutor

def process_connection(source_entity):
    return mapper.map_entity_connections(source_entity)

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(process_connection, all_entities)

all_connections = [conn for result in results for conn in result]
```

### 3. Save and Load Results

```python
import json

# Save connections to file
def save_connections(connections, filepath):
    data = [
        {
            'source_id': c.source_id,
            'target_id': c.target_id,
            'relationship_type': c.relationship_type,
            'strength': c.strength,
            'evidence': c.evidence
        }
        for c in connections
    ]
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

save_connections(connections, 'connections.json')

# Load connections
def load_connections(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return [Connection(**item) for item in data]

loaded_connections = load_connections('connections.json')
```

### 4. Export Network as Graph

```python
import json

def export_network_graph(entities_dict, connections, output_file):
    """Export network in graph format"""
    nodes = []
    edges = []
    
    # Create nodes
    for entity_id, entity in entities_dict.items():
        nodes.append({
            'id': entity_id,
            'label': entity.name,
            'type': entity.entity_type,
            'size': 10 if entity.entity_type == 'firm' else 5
        })
    
    # Create edges
    for conn in connections:
        edges.append({
            'source': conn.source_id,
            'target': conn.target_id,
            'type': conn.relationship_type,
            'strength': conn.strength
        })
    
    graph = {'nodes': nodes, 'edges': edges}
    
    with open(output_file, 'w') as f:
        json.dump(graph, f, indent=2)

export_network_graph(entities_dict, connections, 'network.json')
```

### 5. Query-Specific Connection Discovery

```python
# Find connections for specific query
query = "What infrastructure funds does Blackstone manage?"

# Find relevant entities
relevant_firms = retriever.retrieve_similar_entities(query, k=3)
relevant_funds = retriever.retrieve_by_entity_type('fund', k=5)

# Analyze connections between them
for firm_id, _ in relevant_firms:
    firm = entities_dict[firm_id]
    firm_connections = [
        c for c in connections
        if c.source_id == firm_id and c.target_type == 'fund'
    ]
    
    if firm_connections:
        print(f"\n{firm.name} connections:")
        for conn in firm_connections:
            target_fund = entities_dict.get(conn.target_id)
            print(f"  -> {target_fund.name} (strength: {conn.strength:.2f})")
```

## Performance Optimization

### 1. Configuration Tuning

```python
# In .env or config.py
TOP_K_RESULTS=10          # Retrieve more results
SIMILARITY_THRESHOLD=0.4  # Lower threshold for broader results
CHUNK_SIZE=500            # Smaller chunks for finer granularity
```

### 2. Use Retriever-Only Mode for Speed

```python
# Faster than LLM reasoning
connections = mapper.discover_full_network(
    entities_dict,
    use_llm_reasoning=False  # Use similarity scoring only
)
```

### 3. Pinecone for Scalability

```python
# In .env
VECTOR_STORE_TYPE=pinecone
PINECONE_API_KEY=your-key
PINECONE_INDEX_NAME=linkages
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No API key provided" | Set OPENAI_API_KEY in .env |
| "Vector store not initialized" | Call indexer.index_entities() first |
| Slow connection discovery | Reduce TOP_K_RESULTS, disable LLM reasoning |
| Out of memory | Use Pinecone instead of ChromaDB for large datasets |
| Poor connection quality | Increase SIMILARITY_THRESHOLD or use LLM reasoning |

---

For more examples, see the notebooks directory!
