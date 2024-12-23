from pydantic import BaseModel, ConfigDict

class ParameterEntity(BaseModel):
    pipeline_name: str
    pipeline_id: str
    source_object_name: str
    source_schema_name: str
    pipeline_updated: bool
    
    model_config = ConfigDict(from_attributes=True)