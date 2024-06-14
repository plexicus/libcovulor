from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

import math

FIRST_PAGE = 0
ENTRIES_PER_PAGE = 10

class MongoDBClient:
    def __init__(self, uri="mongodb://mongodb:27017", db_name="plexicus"):
        self.uri = uri
        self.db_name = db_name

    def __enter__(self):
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def get_collection(self, collection_name):
        return self.db[collection_name]
    
# mongo = MongoDBClient()
# Collections
# client_collection = MongoDBClient.get_collection('Client')
# cwes_collection = MongoDBClient.get_collection('CWE')
# with MongoDBClient() as mongo:
#     findings_collection = mongo.get_collection('Finding')
# notifications_collection = MongoDBClient.get_collection('Notification')
# owasps_collection = MongoDBClient.get_collection('OWASP')
# remediation_collection = MongoDBClient.get_collection('Remediation')
# repositories_collection = MongoDBClient.get_collection('Repository')
# rules_collection = MongoDBClient.get_collection('Rules')
# scans_collection = MongoDBClient.get_collection('Scan')
# scan_requests_collection = MongoDBClient.get_collection('ScanRequest')
# users_collection = MongoDBClient.get_collection('Users')
# invitations_collection = MongoDBClient.get_collection('Invitations')

def get_match_query(client_id: str, filters: dict = None) -> dict:
    return {'client_id': client_id,
            **filters}

def delete_one(collection_name: str, client_id: str, _id: str):
    with MongoDBClient() as mongo:
        collection = mongo.get_collection(collection_name)
        query_filter = {"_id": ObjectId(_id), "client_id": client_id}

        try:
            existing_document = collection.find_one(query_filter)

            if not existing_document:
                return None

            result = collection.delete_one(query_filter)
            existing_document["_id"] = str(existing_document["_id"])

            return existing_document if result.deleted_count > 0 else None
        except PyMongoError as e:
            print(f'Error: {e}')

            return None
    
def delete_many(collection_name: str, client_id: str, filters: dict = None):
    with MongoDBClient() as mongo:
        collection = mongo.get_collection(collection_name)
        query_filter = get_match_query(client_id, filters)

        try:
            result = collection.delete_many(query_filter)
            return {"deleted_count": result.deleted_count}
        except PyMongoError as e:
            print(f'Error: {e}')
            return None

def find_many(collection_name: str, client_id: str, options: dict = None):
    with MongoDBClient() as mongo:
        collection = mongo.get_collection(collection_name)
        filters, fields, sort_field, sort_order, paginate, skip, page_size = None, None, None, None, True, FIRST_PAGE, ENTRIES_PER_PAGE

        if options:
            # Filters & Fields
            filters = options.get('filters', None)
            fields = options.get('fields', None)

            # Sorting
            sort_options = options.get('sort', {})
            sort_field = sort_options.get('field', '_id')
            sort_order = sort_options.get('order', 1)

            # Pagination
            pagination_options = options.get('pagination', {})
            paginate = pagination_options.get('paginate', True)
            page_skip = pagination_options.get('page', FIRST_PAGE)
            page_size = pagination_options.get('page_size', ENTRIES_PER_PAGE) if paginate else ENTRIES_PER_PAGE
            skip = max(page_skip * page_size, FIRST_PAGE) if paginate else FIRST_PAGE

        filters_query = get_match_query(client_id, filters)
        total_elements = collection.count_documents(filters_query)
        total_pages = math.ceil(total_elements / page_size) if paginate else 0

        try:
            pagination_meta = {}

            if paginate:
                results = list(collection.find(filters_query, fields).sort(sort_field, sort_order).skip(skip).limit(page_size))
                pagination_meta["pagination"] = {
                    "page": skip // page_size + 1,
                    "pageCount": total_pages,
                    "pageSize": page_size,
                    "total": total_elements
                }
            else:
                results = list(collection.find(filters_query, fields).sort(sort_field, sort_order))

            for result in results:
                result['_id'] = str(result['_id'])

            return {"data": results,
                    "meta": pagination_meta}
        except PyMongoError as e:
            print(f'Error: {e}')

            return None

def find_one(collection_name: str, client_id: str, _id: str):
    with MongoDBClient() as mongo:
        collection = mongo.get_collection(collection_name)
        try:
            result = collection.find_one({"_id": ObjectId(_id),
                                        "client_id": client_id})

            if result is None:
                return None

            result["_id"] = str(result["_id"])

            return result
        except PyMongoError as e:
            print(f'Error: {e}')

            return None

def update_one(collection_name: str, client_id: str, _id: str, data: dict):
    with MongoDBClient() as mongo:
        collection = mongo.get_collection(collection_name)
        query_filter = {"_id": ObjectId(_id), "client_id": client_id}

        try:
            result = collection.update_one(query_filter, {"$set": data})
            existing_document = collection.find_one(query_filter)
            existing_document["_id"] = str(existing_document["_id"])

            return existing_document if result.modified_count > 0 else None
        except PyMongoError as e:
            print(f'Error: {e}')

            return False