"""Linkage mapper for finding connections between entities"""

from typing import List, Dict, Set, Tuple, Optional
from ..data.models import Entity, Connection, Firm, Fund, Deal, ServiceProvider
from ..rag.retriever import EntityRetriever
from ..llm.connector import ConnectionReasoner


class LinkageMapper:
    """Maps and discovers linkages between entities"""
    
    # Define valid connection types
    VALID_CONNECTIONS = {
        ("firm", "fund"): "firm_funds",
        ("fund", "deal"): "fund_deals", 
        ("deal", "service_provider"): "deal_providers",
        ("firm", "service_provider"): "firm_providers",
        ("fund", "service_provider"): "fund_providers",
        ("firm", "deal"): "firm_investments",
    }
    
    def __init__(self, retriever: EntityRetriever, reasoner: ConnectionReasoner):
        self.retriever = retriever
        self.reasoner = reasoner
        self.connections: Dict[str, List[Connection]] = {}
        self.discovered_paths: Dict[str, Dict] = {}
    
    def map_entity_connections(self, source_entity: Entity) -> List[Connection]:
        """Map all connections for a single entity"""
        
        connections = []
        
        # Get potential targets from retriever
        potential_targets = self.retriever.retrieve_connections(source_entity.id)
        
        for target_id, similarity in potential_targets:
            # Try to determine relationship type based on entity types
            connection = self._create_connection(
                source_entity,
                target_id,
                similarity
            )
            if connection:
                connections.append(connection)
                self.connections[source_entity.id] = connections
        
        return connections
    
    def discover_full_network(
        self,
        entities: Dict[str, Entity],
        use_llm_reasoning: bool = True
    ) -> List[Connection]:
        """Discover all connections in the network"""
        
        all_connections = []
        entity_list = list(entities.values())
        
        for source in entity_list:
            for target in entity_list:
                if source.id == target.id:
                    continue
                
                # Check if valid connection type
                key = (source.entity_type, target.entity_type)
                if key not in self.VALID_CONNECTIONS:
                    continue
                
                if use_llm_reasoning:
                    result = self.reasoner.find_connection(source, target)
                    if result.get("is_connected"):
                        connection = Connection(
                            source_id=source.id,
                            target_id=target.id,
                            source_type=source.entity_type,
                            target_type=target.entity_type,
                            relationship_type=self.VALID_CONNECTIONS.get(key, "unknown"),
                            strength=result.get("strength", 0.5),
                            evidence=result.get("evidence", "")
                        )
                        all_connections.append(connection)
                else:
                    # Use retriever-based scoring
                    similarity = self._calculate_similarity(source, target)
                    if similarity > 0.5:
                        connection = Connection(
                            source_id=source.id,
                            target_id=target.id,
                            source_type=source.entity_type,
                            target_type=target.entity_type,
                            relationship_type=self.VALID_CONNECTIONS.get(key, "unknown"),
                            strength=similarity,
                            evidence="Similarity-based connection"
                        )
                        all_connections.append(connection)
        
        return all_connections
    
    def find_shortest_path(
        self,
        source_entity: Entity,
        target_entity: Entity,
        connections: List[Connection],
        max_depth: int = 5
    ) -> Optional[List[Tuple[Entity, Connection]]]:
        """Find shortest path between two entities"""
        
        # Build adjacency list
        graph = self._build_graph(connections)
        
        # BFS to find shortest path
        queue = [(source_entity.id, [])]
        visited = {source_entity.id}
        
        while queue:
            current_id, path = queue.pop(0)
            
            if current_id == target_entity.id:
                return path
            
            if len(path) >= max_depth:
                continue
            
            for connection in graph.get(current_id, []):
                if connection.target_id not in visited:
                    visited.add(connection.target_id)
                    queue.append((connection.target_id, path + [connection]))
        
        return None
    
    def get_entity_neighborhood(
        self,
        entity: Entity,
        connections: List[Connection],
        depth: int = 1
    ) -> Dict[str, List[str]]:
        """Get all connected entities at each depth level"""
        
        neighborhood = {0: [entity.id]}
        current_level = {entity.id}
        
        for d in range(depth):
            next_level = set()
            for entity_id in current_level:
                for conn in connections:
                    if conn.source_id == entity_id:
                        next_level.add(conn.target_id)
                    elif conn.target_id == entity_id:
                        next_level.add(conn.source_id)
            
            if next_level:
                neighborhood[d + 1] = list(next_level)
                current_level = next_level
            else:
                break
        
        return neighborhood
    
    def get_connection_statistics(self, connections: List[Connection]) -> Dict:
        """Calculate statistics about discovered connections"""
        
        stats = {
            "total_connections": len(connections),
            "connections_by_type": {},
            "average_strength": 0,
            "entities_connected": set()
        }
        
        total_strength = 0
        for conn in connections:
            conn_type = conn.relationship_type
            stats["connections_by_type"][conn_type] = \
                stats["connections_by_type"].get(conn_type, 0) + 1
            total_strength += conn.strength
            stats["entities_connected"].add(conn.source_id)
            stats["entities_connected"].add(conn.target_id)
        
        if connections:
            stats["average_strength"] = total_strength / len(connections)
        
        stats["entities_connected"] = len(stats["entities_connected"])
        
        return stats
    
    def _create_connection(
        self,
        source_entity: Entity,
        target_id: str,
        similarity: float
    ) -> Optional[Connection]:
        """Create connection between entities"""
        
        key = (source_entity.entity_type, None)  # Placeholder
        if key not in self.VALID_CONNECTIONS:
            return None
        
        return Connection(
            source_id=source_entity.id,
            target_id=target_id,
            source_type=source_entity.entity_type,
            target_type=None,  # Would be populated from entities dict
            relationship_type=self.VALID_CONNECTIONS.get(key, "unknown"),
            strength=similarity,
            evidence="Retriever-based connection"
        )
    
    def _calculate_similarity(self, source: Entity, target: Entity) -> float:
        """Calculate similarity between entities"""
        # Simple implementation - can be enhanced
        # Check if they share metadata or characteristics
        return 0.5
    
    @staticmethod
    def _build_graph(connections: List[Connection]) -> Dict[str, List[Connection]]:
        """Build adjacency list from connections"""
        graph = {}
        for conn in connections:
            if conn.source_id not in graph:
                graph[conn.source_id] = []
            graph[conn.source_id].append(conn)
        return graph
