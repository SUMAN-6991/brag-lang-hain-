"""Data loader for ingesting entity data"""

import csv
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from .models import Firm, Fund, Deal, ServiceProvider, Connection, Entity


class DataLoader:
    """Loads entity data from various sources"""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path(__file__).parent.parent.parent / "data"
        self.entities: Dict[str, Entity] = {}
        self.connections: List[Connection] = []
    
    def load_csv(self, filename: str, entity_type: str) -> List[Entity]:
        """Load entities from CSV file"""
        filepath = self.data_dir / filename
        entities = []
        
        if not filepath.exists():
            print(f"Warning: {filepath} not found")
            return entities
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                entity = self._create_entity(entity_type, row)
                if entity:
                    entities.append(entity)
                    self.entities[entity.id] = entity
        
        return entities
    
    def load_json(self, filename: str, entity_type: str) -> List[Entity]:
        """Load entities from JSON file"""
        filepath = self.data_dir / filename
        entities = []
        
        if not filepath.exists():
            print(f"Warning: {filepath} not found")
            return entities
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    entity = self._create_entity(entity_type, item)
                    if entity:
                        entities.append(entity)
                        self.entities[entity.id] = entity
        
        return entities
    
    def _create_entity(self, entity_type: str, data: Dict[str, Any]) -> Entity:
        """Create entity object based on type"""
        try:
            if entity_type == "firm":
                return Firm(
                    id=data.get("id"),
                    name=data.get("name"),
                    description=data.get("description", ""),
                    aum=self._parse_float(data.get("aum")),
                    founded_year=self._parse_int(data.get("founded_year")),
                    headquarters=data.get("headquarters"),
                    metadata=data.get("metadata", {})
                )
            elif entity_type == "fund":
                return Fund(
                    id=data.get("id"),
                    name=data.get("name"),
                    description=data.get("description", ""),
                    size=self._parse_float(data.get("size")),
                    fund_type=data.get("fund_type"),
                    vintage_year=self._parse_int(data.get("vintage_year")),
                    managing_firm_id=data.get("managing_firm_id"),
                    metadata=data.get("metadata", {})
                )
            elif entity_type == "deal":
                return Deal(
                    id=data.get("id"),
                    name=data.get("name"),
                    description=data.get("description", ""),
                    deal_type=data.get("deal_type"),
                    deal_value=self._parse_float(data.get("deal_value")),
                    deal_date=self._parse_date(data.get("deal_date")),
                    target_company=data.get("target_company"),
                    investing_fund_id=data.get("investing_fund_id"),
                    metadata=data.get("metadata", {})
                )
            elif entity_type == "service_provider":
                return ServiceProvider(
                    id=data.get("id"),
                    name=data.get("name"),
                    description=data.get("description", ""),
                    service_category=data.get("service_category"),
                    specialization=data.get("specialization"),
                    service_areas=data.get("service_areas", []),
                    metadata=data.get("metadata", {})
                )
        except Exception as e:
            print(f"Error creating {entity_type} from {data}: {e}")
        
        return None
    
    def load_connections_csv(self, filename: str) -> List[Connection]:
        """Load connections from CSV file"""
        filepath = self.data_dir / filename
        connections = []
        
        if not filepath.exists():
            print(f"Warning: {filepath} not found")
            return connections
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    connection = Connection(
                        source_id=row.get("source_id"),
                        target_id=row.get("target_id"),
                        source_type=row.get("source_type"),
                        target_type=row.get("target_type"),
                        relationship_type=row.get("relationship_type"),
                        strength=self._parse_float(row.get("strength", "1.0")),
                        evidence=row.get("evidence", "")
                    )
                    connections.append(connection)
                    self.connections.append(connection)
                except Exception as e:
                    print(f"Error creating connection from {row}: {e}")
        
        return connections
    
    @staticmethod
    def _parse_float(value) -> float:
        """Parse float value"""
        if value is None or value == "":
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def _parse_int(value) -> int:
        """Parse int value"""
        if value is None or value == "":
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def _parse_date(value) -> datetime:
        """Parse date value"""
        if value is None or value == "":
            return None
        try:
            return datetime.fromisoformat(value)
        except (ValueError, TypeError):
            return None
    
    def get_entity(self, entity_id: str) -> Entity:
        """Get entity by ID"""
        return self.entities.get(entity_id)
    
    def get_all_entities(self) -> List[Entity]:
        """Get all loaded entities"""
        return list(self.entities.values())
    
    def get_entities_by_type(self, entity_type: str) -> List[Entity]:
        """Get entities of a specific type"""
        return [e for e in self.entities.values() if e.entity_type == entity_type]
