import pytest
from unittest import mock
from dataliv.domain.repositories.parameter_repository import ParameterRepository
from dataliv.domain.entities.parameter_entity import ParameterEntity

@pytest.fixture
def mock_firestore_connection(mocker):
    return mocker.Mock()

@pytest.fixture
def parameter_repository(mock_firestore_connection):
    return ParameterRepository(mock_firestore_connection)

def test_get_parameter(parameter_repository, mock_firestore_connection):
    mock_firestore_connection.get_collection.return_value.document.return_value.get.return_value.exists = True
    mock_firestore_connection.get_collection.return_value.document.return_value.get.return_value.to_dict.return_value = {
        'pipeline_name': 'test_pipeline',
        'pipeline_id': '123',
        'source_object_name': 'test_object',
        'source_schema_name': 'test_schema',
        'pipeline_updated': True
    }
    result = parameter_repository.get_parameter('test_object', 'test_schema')
    assert result['pipeline_name'] == 'test_pipeline'

def test_get_parameter_not_found(parameter_repository, mock_firestore_connection):
    mock_firestore_connection.get_collection.return_value.document.return_value.get.return_value.exists = False
    result = parameter_repository.get_parameter('nonexistent_object', 'nonexistent_schema')
    assert result is None

# def test_get_parameter_with_error(parameter_repository, mock_firestore_connection):
#     mock_firestore_connection.get_collection.return_value.document.return_value.get.side_effect = Exception("Firestore error")
#     result = parameter_repository.get_parameter('test_object', 'test_schema')
#     assert result is None

def test_set_parameter(parameter_repository, mock_firestore_connection):
    parameter = ParameterEntity(
        pipeline_name='test_pipeline',
        pipeline_id='123',
        source_object_name='test_object',
        source_schema_name='test_schema',
        pipeline_updated=True
    )
    result = parameter_repository.set_parameter(parameter)
    assert result is not None

#tod: add exception no retorno com erro
def test_set_parameter_with_error(parameter_repository, mock_firestore_connection):
    parameter = ParameterEntity(
        pipeline_name='test_pipeline',
        pipeline_id='123',
        source_object_name='test_object',
        source_schema_name='test_schema',
        pipeline_updated=True
    )
    mock_firestore_connection.get_collection.return_value.document.return_value.set.side_effect = Exception("Firestore error")
    result = parameter_repository.set_parameter(parameter)
    assert result is None