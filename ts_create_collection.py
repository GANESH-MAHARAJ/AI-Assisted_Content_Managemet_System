import typesense

# Connect to your Typesense server
client = typesense.Client({
    'api_key': 'xyz',            # Use the same API key you set in the Docker container
    'nodes': [{
        'host': 'localhost',
        'port': '8108',
        'protocol': 'http'
    }],
    'connection_timeout_seconds': 2
})

schema = {
    "name": "pdfs",
    "fields": [
        # Removed 'id' field because Typesense manages document ids internally
        {"name": "file_name", "type": "string", "sort": True},  # Make file_name sortable
        {"name": "tags", "type": "string[]", "facet": True},    # tags are facet enabled
        {"name": "content", "type": "string"}
    ],
    "default_sorting_field": "file_name"  # default sorting by file_name
}

# Delete collection if it already exists (optional)
try:
    client.collections['pdfs'].delete()
    print("Deleted existing 'pdfs' collection.")
except Exception as e:
    print(f"Error deleting collection: {e}")

# Create the collection
client.collections.create(schema)
print("Created 'pdfs' collection successfully.")
