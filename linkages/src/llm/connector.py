"""LLM-based connection reasoning"""

import json
from typing import Dict, List, Optional, Tuple
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from ..config import OPENAI_API_KEY, LLM_MODEL, TEMPERATURE
from ..data.models import Entity, Connection
from .prompts import (
    get_connection_prompt,
    get_explanation_prompt,
    get_linkage_discovery_prompt,
    get_path_finding_prompt
)


class ConnectionReasoner:
    """Uses LLM to reason about entity connections"""
    
    def __init__(self, api_key: str = OPENAI_API_KEY, model: str = LLM_MODEL):
        self.llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=TEMPERATURE
        )
    
    def find_connection(
        self,
        source_entity: Entity,
        target_entity: Entity,
        context: str = ""
    ) -> Dict:
        """Find if connection exists between entities"""
        
        prompt = get_connection_prompt(
            source_entity.name,
            source_entity.entity_type,
            target_entity.name,
            target_entity.entity_type,
            context
        )
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        try:
            # Extract JSON from response
            content = response.content
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = content[json_start:json_end]
                result = json.loads(json_str)
            else:
                result = self._parse_connection_response(content)
        except Exception as e:
            print(f"Error parsing connection response: {e}")
            result = {"is_connected": False, "error": str(e)}
        
        return result
    
    def explain_connection(
        self,
        connection: Connection,
        source_entity: Entity,
        target_entity: Entity
    ) -> str:
        """Generate explanation for a connection"""
        
        prompt = get_explanation_prompt(
            source_entity.name,
            source_entity.entity_type,
            target_entity.name,
            target_entity.entity_type,
            connection.relationship_type
        )
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
    
    def discover_linkages(
        self,
        entity: Entity,
        context: str = ""
    ) -> List[Dict]:
        """Discover all linkages for an entity"""
        
        prompt = get_linkage_discovery_prompt(
            entity.name,
            entity.entity_type,
            context
        )
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        try:
            content = response.content
            json_start = content.find('[')
            json_end = content.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                json_str = content[json_start:json_end]
                linkages = json.loads(json_str)
            else:
                linkages = []
        except Exception as e:
            print(f"Error parsing linkages response: {e}")
            linkages = []
        
        return linkages
    
    def find_connection_path(
        self,
        start_entity: Entity,
        end_entity: Entity
    ) -> Dict:
        """Find connection path between entities"""
        
        prompt = get_path_finding_prompt(
            start_entity.name,
            start_entity.entity_type,
            end_entity.name,
            end_entity.entity_type
        )
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        try:
            content = response.content
            result = self._parse_path_response(content)
        except Exception as e:
            print(f"Error parsing path response: {e}")
            result = {"path": [], "error": str(e)}
        
        return result
    
    @staticmethod
    def _parse_connection_response(content: str) -> Dict:
        """Parse connection response from LLM"""
        result = {
            "is_connected": "yes" in content.lower(),
            "strength": 0.5,
            "relationship_type": "unknown",
            "evidence": content
        }
        
        # Try to extract strength
        if "strength:" in content.lower():
            parts = content.lower().split("strength:")
            if len(parts) > 1:
                strength_str = parts[1].split()[0].strip()
                try:
                    result["strength"] = float(strength_str)
                except:
                    pass
        
        return result
    
    @staticmethod
    def _parse_path_response(content: str) -> Dict:
        """Parse path response from LLM"""
        return {
            "path": [],
            "explanation": content,
            "raw_content": content
        }
