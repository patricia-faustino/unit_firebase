from dataliv.domain.entities.metadata import Metadata
from dataliv.domain.services.parameter_service import ParameterService
from dataliv.domain.repositories.parameter_repository import ParameterRepository
from dataliv.infra.repositories.firestore_connection import FirestoreConnection

class Pipeline:
    def __init__(self, parameter_service: ParameterService):
        self.parameter_service = parameter_service

    def run(self):
        metadata = Metadata(
            pipeline_name='test',
            pipeline_id='test',
            source_object_name='test',
            source_schema_name='test',
            pipeline_updated=False
        )
        self.parameter_service.set_parameter(metadata)
        return True