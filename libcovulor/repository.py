from .database import delete_one, delete_many, find_many, find_one, update_one, MongoDBClient, repositories_collection
from pydantic import BaseModel, Field
from pymongo.errors import PyMongoError

class Repository:
    ACTIVE = 'active'
    AUTH = 'repository_auth'
    BRANCH = 'repository_branch'
    CLIENT_ID = 'client_id'
    DESCRIPTION = 'description'
    ID = 'repository_id'
    NAME = 'alias'
    PRIORITY = 'priority'
    PROCESSING_STATUS = 'processing_status'
    SOURCE_CONTROL = 'source_control'
    TAGS = 'tags'
    TICKET_API_URL = 'ticket_api_url'
    TICKET_AUTH = 'ticket_auth'
    TICKET_PROVIDER_TYPE = 'ticket_provider_type'
    TYPE = 'repository_type'
    URL = 'url'

    @staticmethod
    def create(data: dict):
        try:
            with MongoDBClient() as mongo:
                existing_document = mongo.get_collection(repositories_collection).find_one({Repository.URL: data["uri"]})

                if existing_document:
                    return None

                repo_document = {
                    Repository.ACTIVE: True,
                    Repository.URL: data["uri"],
                    Repository.CLIENT_ID: data[Repository.CLIENT_ID],
                    Repository.TYPE: data["type"],
                    Repository.NAME: data["nickname"],
                    Repository.TICKET_PROVIDER_TYPE: None,
                    Repository.TICKET_AUTH: None,
                    Repository.TICKET_API_URL: None,
                    Repository.DESCRIPTION: data[Repository.DESCRIPTION],
                    Repository.AUTH: data['github_oauth_token'],
                    Repository.PROCESSING_STATUS: "processing",
                    Repository.BRANCH: data["data"]["git_connection"]["repo_branch"],
                    Repository.SOURCE_CONTROL: data[Repository.SOURCE_CONTROL],
                    Repository.PRIORITY: data[Repository.PRIORITY],
                    Repository.TAGS: data[Repository.TAGS]
                }
                repository = mongo.get_collection(repositories_collection).insert_one(repo_document)

                return str(repository.inserted_id) if repository.inserted_id else None
        except PyMongoError as e:
            print(f'Error: {e}')

            return None

    @staticmethod
    def delete(client_id: str, repository_id: str):
        dict_repository = delete_one('Repository', client_id, repository_id)
        # return RepositoryModel.parse_obj(dict_repository)
        return dict_repository

    @staticmethod
    def delete_many(client_id: str, options: dict = None):
        dict_finding = delete_many('Repository', client_id, options)

        return dict_finding

    @staticmethod
    def find_many(client_id: str, options: dict = None):
        repositories = find_many('Repository', client_id, options)
        model_data = []

        for repo in repositories['data']:
            #model_repository = RepositoryModel.parse_obj(repo['attributes'])
            model_repository = repo
            model_data.append(model_repository)

        repositories['data'] = model_data

        return repositories

    @staticmethod
    def find_one(client_id: str, repository_id: str):
        dict_repository = find_one('Repository', client_id, repository_id)
        # return RepositoryModel.parse_obj(dict_repository)
        return dict_repository

    @staticmethod
    def update(client_id: str, repository_id: str, data: dict):
        dict_repository = update_one('Repository', client_id, repository_id, data)
        # return RepositoryModel.parse_obj(dict_finding)
        return dict_repository

class RepositoryModel(BaseModel):
    object_id: str = Field(exclude=True, alias='_id')
