import pymongo
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId


class Finding:
    def __init__(self, mongodb_server: str = "mongodb://mongodb", port: int = 27017, db: str = "plexicus", collection: str = "Finding", client: MongoClient = None):
        if not client:
            self.client = MongoClient(mongodb_server, port)
        else:
            self.client = client
        self.db = self.client[db]
        self.collection = self.db[collection]

    def get_findings_by_client_id(self, client_id: str, options: dict = None):
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
                    page = pagination_options.get('page', 0)
                    page_size = pagination_options.get('page_size', 10)
                else:
                    paginate = True
                    page = 0
                    page_size = 10

                if 'fields' in options:
                    fields = options['fields']
                else:
                    fields = None

                if paginate:
                    page+= 1
                    skip = ((page - 1) * page_size) if ((page - 1) * page_size) >= 0 else 0
                    total_pages = (total_elements+page_size-1)//page_size
                    findings = self.collection.find(query, fields).sort(
                        sort_field, sort_order).skip(skip).limit(page_size)
                else:
                    findings = self.collection.find(
                        query, fields).sort(sort_field, sort_order)
                    total_pages = 0
            else:
                findings = self.collection.find(query)

            for finding in findings:
                finding["_id"] = str(finding["_id"])
                results.append(finding)
            return {"data": results, "meta": {"pagination": {"page": page, "pageSize": page_size, "PageCount": total_pages, "total": total_elements}}}
        except PyMongoError as e:
            print(f'Error: {e}')
            return None

    def get_finding_by_id_and_client_id(self, data: dict):
        try:
            finding = self.collection.find_one({
                "$and": [
                    {"_id": ObjectId(data["finding_id"])},
                    {"client_id": data["client_id"]}
                ]
            })
            if finding is None:
                return None
            finding["_id"] = str(finding["_id"])
            return finding
        except PyMongoError as e:
            print(f'Error: {e}')
            return None

    def create_finding(self, data: dict):
        try:
            existing_document = self.collection.find_one({
                "$and": [
                    {"cwe": data["cwe"]},
                    {"file_path": data["file_path"]},
                    {"original_line": data["original_line"]},
                    {"tool": data["tool"]}
                ]
            })
            if existing_document:
                actual_title = data["title"]
                data.update(existing_document)
                data["title"] = actual_title
                data["duplicate"] = True
                data["duplicate_finding_id"] = str(existing_document["_id"])
                del data["_id"]
            data["processing_status"] = "processing"
            finding = self.collection.insert_one(data)
            if finding.inserted_id:
                return {"id": str(finding.inserted_id), "duplicate": data["duplicate"]}
            else:
                return None
        except PyMongoError as e:
            print(f'Error: {e}')
            return None

    def delete_finding_by_id_and_client_id(self, finding_id: str, client_id: str):
        try:
            existing_document = self.collection.find_one({"$and": [
                {"_id": ObjectId(finding_id)},
                {"client_id": client_id}
            ]})
            if not existing_document:
                return None
            result = self.collection.delete_one(
                {"$and": [
                    {"_id": ObjectId(finding_id)},
                    {"client_id": client_id}
                ]}
            )
            existing_document["_id"] = str(existing_document["_id"])
            return existing_document if result.deleted_count > 0 else None
        except PyMongoError as e:
            print(f'Error: {e}')
            return None

    def update_finding_by_id_and_client_id(self, data: dict, finding_id: str, client_id: str):
        try:
            if not data:
                return None
            result = self.collection.update_one(
                {"$and": [
                    {"_id": ObjectId(finding_id)},
                    {"client_id": client_id}
                ]},
                {"$set": data}
            )
            existing_document = self.collection.find_one({"$and": [
                {"_id": ObjectId(finding_id)},
                {"client_id": client_id}
            ]})
            existing_document["_id"] = str(existing_document["_id"])
            return existing_document if result.modified_count > 0 else None
        except PyMongoError as e:
            print(f'Error: {e}')
            return False

    def close_connection(self):
        self.client.close()
