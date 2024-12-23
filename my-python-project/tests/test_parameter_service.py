import pytest
from unittest import mock
from dataliv.domain.services.parameter_service import ParameterService
from dataliv.domain.entities.metadata import Metadata
from dataliv.domain.entities.parameter_entity import ParameterEntity
from dataliv.domain.repositories.parameter_repository import ParameterRepository

@pytest.fixture
def mock_firestore_connection(mocker):
    return mocker.Mock()

@pytest.fixture
def mock_parameter_repository(mock_firestore_connection, mocker):
    mock_repo = mocker.Mock(spec=ParameterRepository)
    mock_repo.firestore_connection = mock_firestore_connection
    return mock_repo

@pytest.fixture
def parameter_service(mock_parameter_repository):
    return ParameterService(mock_parameter_repository)

def test_set_parameter(parameter_service, mock_parameter_repository):
    metadata = Metadata(
        pipeline_name='test_pipeline',
        pipeline_id='123',
        source_object_name='test_object',
        source_schema_name='test_schema',
        pipeline_updated=True
    )
    parameter_service.set_parameter(metadata)
    assert mock_parameter_repository.set_parameter.called

def test_parameter_exists(parameter_service, mock_parameter_repository):
    mock_parameter_repository.get_parameter.return_value = ParameterEntity(
        pipeline_name='test_pipeline',
        pipeline_id='123',
        source_object_name='test_object',
        source_schema_name='test_schema',
        pipeline_updated=True
    )
    result = parameter_service.parameter_exists(mock_parameter_repository.get_parameter())
    assert result is True

def test_set_parameter_with_existing_parameter(parameter_service, mock_parameter_repository):
    metadata = Metadata(
        pipeline_name='test_pipeline',
        pipeline_id='123',
        source_object_name='test_object',
        source_schema_name='test_schema',
        pipeline_updated=True
    )
    existing_parameter = ParameterEntity(
        pipeline_name='test_pipeline',
        pipeline_id='123',
        source_object_name='test_object',
        source_schema_name='test_schema',
        pipeline_updated=True
    )
    mock_parameter_repository.get_parameter.return_value = existing_parameter
    parameter_service.set_parameter(metadata)
    assert not mock_parameter_repository.set_parameter.called

def test_set_parameter_with_error(parameter_service, mock_parameter_repository):
    metadata = Metadata(
        pipeline_name='test_pipeline',
        pipeline_id='123',
        source_object_name='test_object',
        source_schema_name='test_schema',
        pipeline_updated=True
    )
    mock_parameter_repository.set_parameter.side_effect = Exception("Firestore error")
    with pytest.raises(Exception, match="Firestore error"):
        parameter_service.set_parameter(metadata)

def test_parameter_exists_with_none(parameter_service):
    result = parameter_service.parameter_exists(None)
    assert result is False

def test_is_parameter_saved_equal_parameter_new(parameter_service):
    parameter_new = ParameterEntity(
        pipeline_name='test_pipeline',
        pipeline_id='123',
        source_object_name='test_object',
        source_schema_name='test_schema',
        pipeline_updated=True
    )
    parameter_saved = ParameterEntity(
        pipeline_name='test_pipeline',
        pipeline_id='123',
        source_object_name='test_object',
        source_schema_name='test_schema',
        pipeline_updated=False
    )
    result = parameter_service._ParameterService__is_parameter_saved_equal_parameter_new(parameter_saved, parameter_new)
    assert result is True

def test_is_parameter_saved_not_equal_parameter_new(parameter_service):
    parameter_new = ParameterEntity(
        pipeline_name='test_pipeline',
        pipeline_id='123',
        source_object_name='test_object',
        source_schema_name='test_schema',
        pipeline_updated=True
    )
    parameter_saved = ParameterEntity(
        pipeline_name='test_pipeline',
        pipeline_id='124',
        source_object_name='test_object',
        source_schema_name='test_schema',
        pipeline_updated=False
    )
    result = parameter_service._ParameterService__is_parameter_saved_equal_parameter_new(parameter_saved, parameter_new)
    assert result is False