"""LLM prompts for linkage discovery"""

def get_connection_prompt(
    source_name: str,
    source_type: str,
    target_name: str,
    target_type: str,
    context: str = ""
) -> str:
    """Generate prompt for finding connection between two entities"""
    
    prompt = f"""Analyze the potential connection between the following entities in the alternative markets:

Source Entity:
- Name: {source_name}
- Type: {source_type}

Target Entity:
- Name: {target_name}
- Type: {target_type}

Context Information:
{context}

Based on this information, analyze:
1. Is there a realistic connection between these entities?
2. What type of relationship might exist?
3. How strong is this connection? (Rate 0-1)
4. What evidence supports this connection?

Provide your analysis in JSON format with keys: 
- is_connected (boolean)
- relationship_type (string)
- strength (float 0-1)
- evidence (string)
- explanation (string)
"""
    return prompt


def get_explanation_prompt(
    source_name: str,
    source_type: str,
    target_name: str,
    target_type: str,
    relationship_type: str
) -> str:
    """Generate prompt for explaining a connection"""
    
    prompt = f"""Explain how {source_name} (a {source_type}) connects to {target_name} (a {target_type}).

Connection type: {relationship_type}

Provide a clear, concise explanation of:
1. The nature of this connection
2. How they typically work together in alternative markets
3. Any specific examples or use cases
4. Key contact points or interactions

Keep the explanation professional and factual."""
    
    return prompt


def get_linkage_discovery_prompt(
    entity_name: str,
    entity_type: str,
    context: str = ""
) -> str:
    """Generate prompt for discovering all linkages for an entity"""
    
    prompt = f"""Find all significant linkages for the following entity in the alternative markets:

Entity:
- Name: {entity_name}
- Type: {entity_type}

Context:
{context}

Identify:
1. Direct connections (firms to funds, funds to deals, deals to service providers)
2. Indirect connections (chains of relationships)
3. Common connection patterns
4. Key relationship types

For each connection found, provide:
- Connected entity type
- Relationship type
- Connection strength (0-1)
- Brief explanation

Format as JSON with array of connections."""
    
    return prompt


def get_path_finding_prompt(
    start_entity: str,
    start_type: str,
    end_entity: str,
    end_type: str
) -> str:
    """Generate prompt for finding path between entities"""
    
    prompt = f"""Find the connection path between these two entities in alternative markets:

Starting Point:
- Name: {start_entity}
- Type: {start_type}

Ending Point:
- Name: {end_entity}
- Type: {end_type}

Possible intermediate entity types: firm, fund, deal, service_provider

Trace the most likely path:
1. What intermediate entities would connect these?
2. In what order would they connect?
3. How strong are each connection link?
4. What is the overall path strength?

Provide the path as a sequence of connections with explanations."""
    
    return prompt
