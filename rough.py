import os
from pymongo import MongoClient

# Connect to your MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.pdf_tags
collection = db.tagged_files

def clean_filenames_in_db():
    documents = collection.find({})
    for doc in documents:
        original_filename = doc.get('file_name', '')
        # Normalize path separators (handle / or \)
        base_filename = os.path.basename(original_filename)
        if base_filename != original_filename:
            print(f"Updating: {original_filename} -> {base_filename}")
            collection.update_one(
                {'_id': doc['_id']},
                {'$set': {'file_name': base_filename}}
            )

if __name__ == "__main__":
    clean_filenames_in_db()
    print("Filename cleanup completed.")
