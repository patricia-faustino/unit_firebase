from dataliv.domain.entities.parameter_entity import ParameterEntity
from dataliv.domain.repositories.parameter_repository import ParameterRepository

class ParameterService:
    def __init__(self, parameter_repository: ParameterRepository):
        self.parameter_repository = parameter_repository

    def set_parameter(self, metadata: ParameterEntity):
        source_object_name = metadata.source_object_name
        source_schema_name = metadata.source_schema_name
        existing_parameter = self.parameter_repository.get_parameter(source_object_name, source_schema_name)
        if not self.__is_parameter_saved_equal_parameter_new(existing_parameter, metadata):
            self.parameter_repository.set_parameter(metadata)

    def __is_parameter_saved_equal_parameter_new(self, parameter_table_saved: ParameterEntity, parameter_table: ParameterEntity) -> bool:
        if parameter_table_saved is None:
            return False
        return parameter_table_saved.pipeline_id == parameter_table.pipeline_id

    def parameter_exists(self, parameter_table_saved: ParameterEntity) -> bool:
        return parameter_table_saved is not None