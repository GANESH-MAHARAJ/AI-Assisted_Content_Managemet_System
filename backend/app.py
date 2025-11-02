import sys
import os
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import typesense
from flask_cors import CORS
import re
from urllib.parse import unquote

# Import Ollama LLM client here
from langchain_ollama import OllamaLLM

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

UPLOAD_FOLDER = r'C:\InternShip\SSPL_CMS\SAMPELproject\arxiv_pdfs'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client.pdf_tags
collection = db.tagged_files

typesense_client = typesense.Client({
    'api_key': 'xyz',
    'nodes': [{
        'host': 'localhost',
        'port': '8108',
        'protocol': 'http'
    }],
    'connection_timeout_seconds': 2
})

def extract_text_from_pdf(file_path):
    from PyPDF2 import PdfReader
    try:
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return text
    except Exception as e:
        print(f'Error extracting text: {e}')
        return ''

def clean_tags(raw_tags):
    cleaned = []
    for line in raw_tags:
        line = re.sub(r'^\s*\d+\.\s*', '', line)
        line = re.sub(r'^\s*[\*\-\+]?\s*', '', line)
        line = re.sub(r'(\*\*|__|\*)', '', line)
        line = line.rstrip(':')
        line = line.strip()
        if line and not line.lower().startswith(('here are', 'these tags', 'subfields', 'algorithms', 'applications')):
            cleaned.append(line)
    seen = set()
    cleaned_unique = []
    for tag in cleaned:
        if tag not in seen:
            cleaned_unique.append(tag)
            seen.add(tag)
    return cleaned_unique

def generate_tags_for_text(text: str) -> list:
    llm = OllamaLLM(model="llama3.1:latest")
    prompt =         print(f'Error indexing {base_filename} to Typesense: {e}')

    response = llm.invoke(prompt)
    raw_tags = response.strip().split("\n")
    cleaned_tags = clean_tags(raw_tags)
    return cleaned_tags

def store_in_mongo(file_name, content, tags):
    base_filename = os.path.basename(file_name)
    doc = {
        'file_name': base_filename,
        'content': content,
        'tags': tags
    }
    collection.insert_one(doc)
    print(f'Successfully stored {base_filename} in MongoDB.')

def add_document_to_typesense(file_name, tags, content):
    base_filename = os.path.basename(file_name)
    doc = {
        'id': base_filename,
        'file_name': base_filename,
        'tags': tags,
        'content': content
    }
    try:
        response = typesense_client.collections['pdfs'].documents.upsert(doc)
        print(f'Indexed {base_filename} to Typesense: {response}')
    except Exception as e:
        print(f'Error indexing {base_filename} to Typesense: {e}')

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file part'}), 400

    pdf_file = request.files['pdf']
    if pdf_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(pdf_file.filename)

    # Check for duplicates in the database
    existing_file = collection.find_one({'file_name': filename})
    if existing_file:
        return jsonify({'error': 'PDF already exists'}), 409  # HTTP 409 Conflict

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        pdf_file.save(filepath)
        text = extract_text_from_pdf(filepath)
        if not text.strip():
            os.remove(filepath)
            return jsonify({'error': 'PDF text extraction failed or empty'}), 400

        tags = generate_tags_for_text(text)

        store_in_mongo(filename, text[:], tags)
        add_document_to_typesense(filename, tags, text[:2000])

        return jsonify({'message': f'File {filename} uploaded and processed successfully.'})
    except Exception as e:
        return jsonify({'error': f'Failed to process file: {str(e)}'}), 500

@app.route('/search_pdfs', methods=['GET'])
def search_pdfs():
    keywords = request.args.get('keywords', '')
    if not keywords:
        return jsonify({'error': 'No keywords provided'}), 400
    results = perform_search(keywords)
    return jsonify({'results': results}), 200


@app.route('/get_pdf/<path:filename>', methods=['GET'])  # Accept slashes and full path parts
def get_pdf(filename):
    decoded_filename = unquote(filename)  # Decode %20 to space etc.
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], decoded_filename)
    print(f"Decoded filename: {decoded_filename}")
    print(f"Looking for file at: {filepath}")
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return jsonify({'error': 'File not found'}), 404
    return send_file(filepath, as_attachment=False, mimetype='application/pdf')


def perform_search(keywords):
    try:
        search_parameters = {
            'q': keywords,
            'query_by': 'file_name,tags,content',
            'sort_by': '_text_match:desc',
            'per_page': 20
        }
        results = typesense_client.collections['pdfs'].documents.search(search_parameters)
        hits = results.get('hits', [])
        search_results = []
        for hit in hits:
            doc = hit['document']
            file_name = os.path.basename(doc.get('file_name', ''))
            search_results.append({
                'file_name': file_name, 
                'tags': doc.get('tags', [])
            })
        return search_results
    except Exception as e:
        print(f"Typesense search error: {e}")
        return []

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f'Error running the server: {e}')
