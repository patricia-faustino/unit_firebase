import pytest
from unittest import mock
from dataliv.infra.repositories.firestore_connection import FirestoreConnection

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv('FIRESTORE_CERTIFICATE', '{"type": "service_account", "project_id": "test_project", "client_email": "test@test.com", "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBeMwggXfAgEAAoIBAQCl1b...\\n-----END PRIVATE KEY-----\\n", "token_uri": "https://oauth2.googleapis.com/token"}')
    monkeypatch.setenv('FIRESTORE_DB_ID', 'firestore_db_id')
    monkeypatch.setenv('FIRESTORE_COLLECTION_DB', 'collection_db')

@pytest.fixture
def mock_settings(mocker):
    settings = mocker.patch('dataliv.infra.repositories.firestore_connection.settings')
    settings.firestore_certificate = '{"type": "service_account", "project_id": "test_project", "client_email": "test@test.com", "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBeMwggXfAgEAAoIBAQCl1b...\\n-----END PRIVATE KEY-----\\n", "token_uri": "https://oauth2.googleapis.com/token"}'
    settings.firestore_db_id = 'firestore_db_id'
    settings.firestore_collection_db = 'collection_db'
    return settings

@pytest.fixture
def mock_firebase_admin(mocker):
    mock_firebase_admin = mocker.patch('dataliv.infra.repositories.firestore_connection.firebase_admin')
    mock_firebase_admin.initialize_app.return_value = None
    return mock_firebase_admin

@pytest.fixture
def mock_firestore(mocker):
    mock_firestore = mocker.patch('dataliv.infra.repositories.firestore_connection.firestore')
    mock_firestore.client.return_value.collection.return_value = mocker.Mock()
    return mock_firestore

@pytest.fixture
def mock_credentials(mocker):
    mock_credentials = mocker.patch('dataliv.infra.repositories.firestore_connection.credentials.Certificate')
    mock_credentials.return_value = mocker.Mock()
    return mock_credentials

@pytest.fixture
def firestore_connection(mock_settings, mock_firebase_admin, mock_credentials, mock_firestore):
    return FirestoreConnection()

def test_initialize(firestore_connection):
    result = firestore_connection.initialize()
    assert result is not None

def test_get_collection(firestore_connection):
    result = firestore_connection.get_collection()
    assert result is not None

def test_initialize_with_invalid_certificate(mocker, mock_firebase_admin, mock_firestore):
    mock_settings = mocker.patch('dataliv.infra.repositories.firestore_connection.settings')
    mock_settings.firestore_certificate = '{"type": "service_account", "project_id": "test_project", "client_email": "test@test.com", "private_key": "INVALID_KEY", "token_uri": "https://oauth2.googleapis.com/token"}'
    mock_settings.firestore_db_id = 'firestore_db_id'
    mock_settings.firestore_collection_db = 'collection_db'
    
    with pytest.raises(ValueError, match="Failed to initialize a certificate credential"):
        FirestoreConnection()

def test_initialize_with_missing_certificate(mocker, mock_firebase_admin, mock_firestore):
    mock_settings = mocker.patch('dataliv.infra.repositories.firestore_connection.settings')
    mock_settings.firestore_certificate = None
    mock_settings.firestore_db_id = 'firestore_db_id'
    mock_settings.firestore_collection_db = 'collection_db'
    
    with pytest.raises(ValueError, match="Firestore certificate is not set"):
        FirestoreConnection()

def test_get_collection_with_firestore_error(mocker, mock_firebase_admin, mock_credentials):
    mock_settings = mocker.patch('dataliv.infra.repositories.firestore_connection.settings')
    mock_settings.firestore_certificate = '{"type": "service_account", "project_id": "test_project", "client_email": "test@test.com", "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBeMwggXfAgEAAoIBAQCl1b...\\n-----END PRIVATE KEY-----\\n", "token_uri": "https://oauth2.googleapis.com/token"}'
    mock_settings.firestore_db_id = 'firestore_db_id'
    mock_settings.firestore_collection_db = 'collection_db'
    
    mock_firestore = mocker.patch('dataliv.infra.repositories.firestore_connection.firestore')
    mock_firestore.client.side_effect = Exception("Firestore error")
    
    with pytest.raises(ValueError, match="Failed to initialize a certificate credential"):
        FirestoreConnection()
