import pytest

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv('FIRESTORE_CERTIFICATE', '{"type": "service_account", "project_id": "test_project"}')
    monkeypatch.setenv('FIRESTORE_DB_ID', 'firestore_db_id')
    monkeypatch.setenv('FIRESTORE_COLLECTION_DB', 'collection_db')