import pytest
from unittest.mock import patch, MagicMock
from libcovulor.repository import Repository

@pytest.fixture
def mock_db(mocker):
    mock_collection = mocker.patch('libcovulor.repository.repositories_collection')
    return mock_collection

def test_create_repository(mock_db):
    data = {
        "uri": "http://example.com/repo.git",
        "client_id": "123",
        "type": "git",
        "nickname": "example_repo",
        "description": "An example repository",
        "github_oauth_token": "token",
        "data": {
            "git_connection": {
                "repo_branch": "main"
            }
        },
        "source_control": "github",
        "priority": "high",
        "tags": ["example", "repo"]
    }

    mock_db.find_one.return_value = None
    mock_db.insert_one.return_value.inserted_id = "507f1f77bcf86cd799439011"

    result = Repository.create(data)

    assert result == "507f1f77bcf86cd799439011"
    mock_db.find_one.assert_called_once_with({Repository.URL: data["uri"]})
    mock_db.insert_one.assert_called_once()

def test_create_repository_already_exists(mock_db):
    data = {"uri": "http://example.com/repo.git"}
    mock_db.find_one.return_value = {"_id": "507f1f77bcf86cd799439011"}

    result = Repository.create(data)

    assert result is None
    mock_db.find_one.assert_called_once_with({Repository.URL: data["uri"]})

def test_delete_repository(mock_db):
    client_id = "123"
    repository_id = "507f1f77bcf86cd799439011"
    mock_db.delete_one.return_value = {"deleted_count": 1}

    with patch('libcovulor.repository.delete_one', return_value={"deleted_count": 1}) as mock_delete_one:
        result = Repository.delete(client_id, repository_id)

        assert result == {"deleted_count": 1}
        mock_delete_one.assert_called_once_with(mock_db, client_id, repository_id)

def test_find_many_repositories(mock_db):
    client_id = "123"
    options = None
    mock_db.find.return_value = {"data": [{"attributes": {"name": "repo1"}}, {"attributes": {"name": "repo2"}}]}

    with patch('libcovulor.repository.find_many', return_value={"data": [{"attributes": {"name": "repo1"}}, {"attributes": {"name": "repo2"}}]}) as mock_find_many:
        result = Repository.find_many(client_id, options)

        assert "data" in result
        assert len(result["data"]) == 2
        mock_find_many.assert_called_once_with(mock_db, client_id, options)

def test_find_one_repository(mock_db):
    client_id = "123"
    repository_id = "507f1f77bcf86cd799439011"
    mock_db.find_one.return_value = {"_id": repository_id, "name": "repo1"}

    with patch('libcovulor.repository.find_one', return_value={"_id": repository_id, "name": "repo1"}) as mock_find_one:
        result = Repository.find_one(client_id, repository_id)

        assert result == {"_id": repository_id, "name": "repo1"}
        mock_find_one.assert_called_once_with(mock_db, client_id, repository_id)

def test_update_repository(mock_db):
    client_id = "123"
    repository_id = "507f1f77bcf86cd799439011"
    data = {"name": "updated_repo"}
    mock_db.update_one.return_value = {"modified_count": 1}

    with patch('libcovulor.repository.update_one', return_value={"modified_count": 1}) as mock_update_one:
        result = Repository.update(client_id, repository_id, data)

        assert result == {"modified_count": 1}
        mock_update_one.assert_called_once_with(mock_db, client_id, repository_id, data)