from pydantic import BaseModel, Field
from typing import Optional

from ....response_models.base_models import SerializableModel

class BiosampleCharacteristics(SerializableModel, BaseModel):
    life_stage: Optional[str] = Field(default=None, description='donor/sample life stage: adult, fetal, embryo')
    biosample_term: Optional[str] = Field(default=None, description='mapped ontology term')
    system_category: Optional[str] = None
    tissue_category: Optional[str] = None
    biosample_display: Optional[str] = None
    biosample_summary: Optional[str] = None
    biosample_term_id: Optional[str] = Field(default=None, description='mapped ontology term identifier')
    
    