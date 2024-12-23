from pydantic import BaseModel


class Metadata(BaseModel):
    pipeline_name: str
    pipeline_id: str
    source_object_name: str
    source_schema_name: str
    pipeline_updated: bool
