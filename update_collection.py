import typesense

# Typesense client configuration
client = typesense.Client({
    'api_key': 'xyz',  # Same API key as before
    'nodes': [{
        'host': 'localhost',
        'port': '8108',
        'protocol': 'http'
    }],
    'connection_timeout_seconds': 2
})

try:
    # Delete existing collection (if any)
    client.collections['pdfs'].delete()
    print("Deleted existing 'pdfs' collection.")

    # Create collection with sortable file_name
    schema = {
        'name': 'pdfs',
        'fields': [
            {'name': 'file_name', 'type': 'string', 'facet': False, 'sort': True},
            {'name': 'content', 'type': 'string', 'facet': False},
            {'name': 'tags', 'type': 'string[]', 'facet': True}
        ],
        'default_sorting_field': 'file_name'
    }

    client.collections.create(schema)
    print("Updated 'pdfs' collection with sortable file_name.")
except Exception as e:
    print(f"Error updating collection: {e}")
