import pytest
from unittest import mock
from dataliv.domain.entities.pipeline import Pipeline
from dataliv.domain.entities.metadata import Metadata
from dataliv.domain.services.parameter_service import ParameterService
from dataliv.domain.repositories.parameter_repository import ParameterRepository
from dataliv.infra.repositories.firestore_connection import FirestoreConnection

@pytest.fixture
def mock_firestore_connection(mocker):
    return mocker.Mock()

@pytest.fixture
def mock_parameter_repository(mock_firestore_connection, mocker):
    mock_repo = mocker.Mock(spec=ParameterRepository)
    mock_repo.firestore_connection = mock_firestore_connection
    return mock_repo

@pytest.fixture
def mock_parameter_service(mock_parameter_repository, mocker):
    return mocker.Mock(spec=ParameterService)

@pytest.fixture
def pipeline(mock_parameter_service):
    pipeline = Pipeline(parameter_service=mock_parameter_service)
    return pipeline

def test_pipeline_run(pipeline, mock_parameter_service):
    result = pipeline.run()
    assert result is True
    assert mock_parameter_service.set_parameter.called

def test_pipeline_run_with_error(mocker, pipeline, mock_parameter_service):
    mock_parameter_service.set_parameter.side_effect = Exception("Firestore error")
    with pytest.raises(Exception, match="Firestore error"):
        pipeline.run()