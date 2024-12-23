from pydantic import ValidationError
import pytest
from dataliv.domain.entities.parameter_entity import ParameterEntity

def test_parameter_entity_creation():
    parameter = ParameterEntity(
        pipeline_name='test_pipeline',
        pipeline_id='123',
        source_object_name='test_object',
        source_schema_name='test_schema',
        pipeline_updated=True
    )
    assert parameter.pipeline_name == 'test_pipeline'
    assert parameter.pipeline_id == '123'
    assert parameter.source_object_name == 'test_object'
    assert parameter.source_schema_name == 'test_schema'
    assert parameter.pipeline_updated is True

def test_parameter_entity_validation_error():
    with pytest.raises(ValidationError):
        ParameterEntity(
            pipeline_name='test_pipeline',
            pipeline_id='123',
            source_object_name='test_object',
            source_schema_name='test_schema',
            pipeline_updated='not_a_bool'
        )