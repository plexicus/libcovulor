from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
import os


class Repository:
    def __init__(self):
        self.client = MongoClient(
            os.getenv('MONGODB_SERVER', 'mongodb://mongodb:27017/'))
        self.db = self.client[os.getenv('MONGO_DB', 'plexicus')]
        self.collection = self.db[os.getenv(
            'MONGO_COLLECTION_REPOSITORY', 'Repository')]

    def get_repository_by_id_and_client_id(self, data: dict):
        try:
            repository = self.collection.find_one({
                "$and": [
                    {"_id": ObjectId(data["repository_id"])},
                    {"client_id": data["client_id"]}
                ]
            })
            if repository is None:
                return None
            repository["_id"] = str(repository["_id"])
            return repository
        except PyMongoError as e:
            print(f'Error: {e}')
            return None

    def create_repository(self, data: dict):
        try:
            existing_document = self.collection.find_one({"url": data["uri"]})
            if existing_document:
                return None
            repo_document = {
                "active": True,
                "url": data["uri"],
                "client_id": data["client_id"],
                "repository_type": data["type"],
                "alias": data["nickname"],
                "ticket_provider_type": None,
                "ticket_auth": None,
                "ticket_api_url": None,
                "description": data["description"],
                "repository_auth": data['github_oauth_token'],
                "processing_status": "processing",
                "repository_branch": data["data"]["git_connection"]["repo_branch"]
            }
            repository = self.collection.insert_one(repo_document)
            if repository.inserted_id:
                return str(repository.inserted_id)
            else:
                return None
        except PyMongoError as e:
            print(f'Error: {e}')
            return None
        
    def delete_repository_by_id_and_client_id(self, repository_id: str, client_id: str):
        try:
            result = self.collection.delete_one(
                {"$and": [
                    {"_id": ObjectId(repository_id)},
                    {"client_id": client_id}
                ]}
            )
            return True if result.deleted_count > 0 else None
        except PyMongoError as e:
            print(f'Error: {e}')
            return None
    
    def close_connection(self):
        self.client.close()
