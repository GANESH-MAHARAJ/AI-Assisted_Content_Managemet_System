import typesense

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

def search_pdfs(keywords):
    try:
        # Split keywords to list to filter tags as well
        keyword_list = keywords.split()

        # Build filter_by clause to match any tag
        # This will return documents where tags contains at least one of the keywords
        if keyword_list:
            filter_by = " || ".join([f'tags:="{kw}"' for kw in keyword_list])
        else:
            filter_by = ""

        # Build search parameters
        search_parameters = {
            'q': keywords,
            'query_by': 'content',    # Search content fully
            'sort_by': 'file_name:asc',
            'num_typos': 1,
            'page': 1,
            'per_page': 10
        }

        # Add filter_by only if non-empty
        if filter_by:
            search_parameters['filter_by'] = filter_by

        # Execute the search
        results = typesense_client.collections['pdfs'].documents.search(search_parameters)

        # Display the results
        if results['hits']:
            for hit in results['hits']:
                doc = hit['document']
                print(f"File: {doc['file_name']}, Tags: {', '.join(doc['tags'])}")
        else:
            print("No matching documents found.")

    except Exception as e:
        print(f"Error during search: {e}")

# Example usage
keywords = input("Enter keywords to search for: ")
search_pdfs(keywords)
