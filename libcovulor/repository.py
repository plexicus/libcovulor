import pymongo
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId


class Repository:
    def __init__(self, mongodb_server: str = "mongodb://mongodb", port: int = 27017, db: str = "plexicus", collection: str = "Repository", client: MongoClient = None):
        if not client:
            self.client = MongoClient(mongodb_server, port)
        else:
            self.client = client
        self.db = self.client[db]
        self.collection = self.db[collection]

    def get_repositories_by_client_id(self, client_id: str, options: dict = None):
        try:
            results = []
            query = {"client_id": client_id}
            if options:
                if 'filters' in options:
                    query.update(options['filters'])

                total_elements = self.collection.count_documents(query)

                sort_options = options.get('sort', None)

                if sort_options:
                    sort_field = sort_options.get('field', '_id')
                    sort_order = sort_options.get('order', 1)
                    sort_order = pymongo.ASCENDING if sort_order == 1 else pymongo.DESCENDING
                else:
                    sort_field = '_id'
                    sort_order = pymongo.ASCENDING

                if 'pagination' in options:
                    pagination_options = options['pagination']
                    paginate = pagination_options.get('paginate', True)
                    page = pagination_options.get('page', 1)
                    page_size = pagination_options.get('page_size', 10)
                else:
                    paginate = True
                    page = 1
                    page_size = 10

                if 'fields' in options:
                    fields = options['fields']
                else:
                    fields = None

                if paginate:
                    skip = (page - 1) * page_size
                    total_pages = (total_elements+page_size-1)//page_size
                    repositories = self.collection.find(query, fields).sort(
                        sort_field, sort_order).skip(skip).limit(page_size)
                else:
                    repositories = self.collection.find(
                        query, fields).sort(sort_field, sort_order)
                    total_pages = 0
            else:
                repositories = self.collection.find(query)

            for repository in repositories:
                repository["_id"] = str(repository["_id"])
                results.append(repository)
            return {"data": results, "meta": {"pagination": {"page": page, "pageSize": page_size, "PageCount": total_pages, "total": total_elements}}}
        except PyMongoError as e:
            print(f'Error: {e}')
            return None

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
            existing_document = self.collection.find_one({"$and": [
                {"_id": ObjectId(repository_id)},
                {"client_id": client_id}
            ]})
            if not existing_document:
                return None
            result = self.collection.delete_one(
                {"$and": [
                    {"_id": ObjectId(repository_id)},
                    {"client_id": client_id}
                ]}
            )
            return existing_document if result.deleted_count > 0 else None
        except PyMongoError as e:
            print(f'Error: {e}')
            return None

    def update_repository_by_id_and_client_id(self, data: dict, repository_id: str, client_id: str):
        try:
            if not data:
                return None
            result = self.collection.update_one(
                {"$and": [
                    {"_id": ObjectId(repository_id)},
                    {"client_id": client_id}
                ]},
                {"$set": data}
            )
            return True if result.modified_count > 0 else None
        except PyMongoError as e:
            print(f'Error: {e}')
            return False

    def close_connection(self):
        self.client.close()
