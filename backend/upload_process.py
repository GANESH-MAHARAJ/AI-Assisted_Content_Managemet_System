import os
import shutil
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import typesense

# Initialize Flask app
app = Flask(__name__)

# Configure folders
TEMP_FOLDER = 'temp_uploads'

# Set permanent folder outside backend (adjust the path as per your environment)
PERMANENT_FOLDER = r'C:\SSPL_CMS\SAMPELproject\arxiv_pdfs'  # <--- external permanent folder path

os.makedirs(TEMP_FOLDER, exist_ok=True)
os.makedirs(PERMANENT_FOLDER, exist_ok=True)

# MongoDB client setup
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client.pdf_tags
collection = db.tagged_files

# Typesense client setup
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


def generate_tags_for_text(text):
    # Replace with your actual tagging logic/LLM call
    return ['example', 'tags', 'from', 'text']


def store_in_mongo(file_name, content, tags):
    doc = {
        'file_name': file_name,
        'content': content,
        'tags': tags
    }
    collection.insert_one(doc)
    print(f'Successfully stored {file_name} in MongoDB.')


def add_document_to_typesense(file_name, tags, content):
    doc = {
        'id': file_name,
        'file_name': file_name,
        'tags': tags,
        'content': content
    }
    try:
        response = typesense_client.collections['pdfs'].documents.upsert(doc)
        print(f'Indexed {file_name} to Typesense: {response}')
    except Exception as e:
        print(f'Error indexing {file_name} to Typesense: {e}')


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file part'}), 400

    pdf_file = request.files['pdf']
    if pdf_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(pdf_file.filename)

    # Save to temp folder first
    temp_path = os.path.join(TEMP_FOLDER, filename)
    pdf_file.save(temp_path)

    # Extract text
    text = extract_text_from_pdf(temp_path)
    if not text.strip():
        os.remove(temp_path)
        return jsonify({'error': 'PDF text extraction failed or empty'}), 400

    # Generate tags
    tags = generate_tags_for_text(text)

    # Store in MongoDB
    store_in_mongo(filename, text[:2000], tags)

    # Add document to Typesense
    add_document_to_typesense(filename, tags, text[:2000])

    # Move PDF to permanent storage outside backend
    permanent_path = os.path.join(PERMANENT_FOLDER, filename)
    shutil.move(temp_path, permanent_path)

    return jsonify({'message': f'{filename} uploaded, processed, and stored successfully.'}), 200


if __name__ == '__main__':
    app.run(debug=True)
