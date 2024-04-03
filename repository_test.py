from libcovulor import Repository
import os

repo = Repository()

data_create = {
    "active": True,
    "client_id": "65f079f3ef898e6a6bb37e5b",
    "nickname": "plexicus/simple-vulnerable",
    "description": "",
    "uri": "https://github.com/plexicus/simple-vulnerable",
    "type": "git_repository",
    "github_oauth_token": os.getenv('TOKEN', ''),
    "data": {
        "git_connection": {
            "repo_url": "https://github.com/plexicus/simple-vulnerable",
            "repo_token": "",
            "repo_branch": "main"
        }
    }
}
print("---------------------- Repository create")
id = repo.create_repository(data_create)
print(id)

print("---------------------- Repository by id and client id")
print(repo.get_repository_by_id_and_client_id(
    {'repository_id': id, 'client_id': '65f079f3ef898e6a6bb37e5b'}))

print("---------------------- Repository delete")
print(repo.delete_repository_by_id_and_client_id(id, '65f079f3ef898e6a6bb37e5b'))
repo.close_connection()
