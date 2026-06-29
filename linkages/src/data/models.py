"""Data models for entities and connections"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class Entity(BaseModel):
    """Base class for all entities"""
    
    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Entity name")
    description: str = Field(..., description="Entity description")
    entity_type: str = Field(..., description="Type of entity")
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "firm_001",
                "name": "Example Firm",
                "description": "A leading investment firm",
                "entity_type": "firm",
                "metadata": {"aum": "$10B", "founded": 2010}
            }
        }


class Firm(Entity):
    """Investment firm entity"""
    
    aum: Optional[float] = Field(None, description="Assets under management in millions")
    founded_year: Optional[int] = Field(None, description="Year founded")
    headquarters: Optional[str] = Field(None, description="Headquarters location")
    
    def __init__(self, **data):
        if "entity_type" not in data:
            data["entity_type"] = "firm"
        super().__init__(**data)


class Fund(Entity):
    """Investment fund entity"""
    
    size: Optional[float] = Field(None, description="Fund size in millions")
    fund_type: Optional[str] = Field(None, description="Type of fund (e.g., PE, VC, Hedge)")
    vintage_year: Optional[int] = Field(None, description="Fund vintage year")
    managing_firm_id: Optional[str] = Field(None, description="ID of managing firm")
    
    def __init__(self, **data):
        if "entity_type" not in data:
            data["entity_type"] = "fund"
        super().__init__(**data)


class Deal(Entity):
    """Investment deal entity"""
    
    deal_type: Optional[str] = Field(None, description="Type of deal (e.g., acquisition, investment)")
    deal_value: Optional[float] = Field(None, description="Deal value in millions")
    deal_date: Optional[datetime] = Field(None, description="Date of deal")
    target_company: Optional[str] = Field(None, description="Target company name")
    investing_fund_id: Optional[str] = Field(None, description="ID of investing fund")
    
    def __init__(self, **data):
        if "entity_type" not in data:
            data["entity_type"] = "deal"
        super().__init__(**data)


class ServiceProvider(Entity):
    """Service provider entity"""
    
    service_category: Optional[str] = Field(None, description="Category of service (e.g., Legal, Advisory, Tech)")
    specialization: Optional[str] = Field(None, description="Specific specialization")
    service_areas: Optional[List[str]] = Field(None, description="Areas of service")
    
    def __init__(self, **data):
        if "entity_type" not in data:
            data["entity_type"] = "service_provider"
        super().__init__(**data)


class Connection(BaseModel):
    """Represents a connection between two entities"""
    
    source_id: str = Field(..., description="ID of source entity")
    target_id: str = Field(..., description="ID of target entity")
    source_type: str = Field(..., description="Type of source entity")
    target_type: str = Field(..., description="Type of target entity")
    relationship_type: str = Field(..., description="Type of relationship")
    strength: float = Field(default=1.0, ge=0, le=1.0, description="Connection strength (0-1)")
    evidence: str = Field(default="", description="Evidence supporting the connection")
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "source_id": "firm_001",
                "target_id": "fund_001",
                "source_type": "firm",
                "target_type": "fund",
                "relationship_type": "firm_funds",
                "strength": 0.95,
                "evidence": "Firm ABC manages Fund XYZ"
            }
        }
