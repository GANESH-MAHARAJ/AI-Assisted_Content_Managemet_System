from pymongo import MongoClient
import typesense

# MongoDB connection
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client.pdf_tags
collection = db.tagged_files

# Typesense connection
typesense_client = typesense.Client({
    'api_key': 'xyz',  # Use the same API key you set in the Docker container
    'nodes': [{
        'host': 'localhost',
        'port': '8108',
        'protocol': 'http'
    }],
    'connection_timeout_seconds': 2
})

# Fetch documents from MongoDB
documents = collection.find()

for doc in documents:
    try:
        # Prepare the document for Typesense
        typesense_document = {
            "id": str(doc["_id"]),  # Use MongoDB's unique ID
            "file_name": doc.get("file_name", ""),
            "tags": doc.get("tags", []),
            "content": doc.get("content", "")
        }

        # Index the document in Typesense
        response = typesense_client.collections['pdfs'].documents.create(typesense_document)
        print(f"Indexed document: {typesense_document['file_name']} -> {response}")
    except Exception as e:
        print(f"Error indexing document {doc.get('file_name')}: {e}")

print("All documents indexed successfully.")
