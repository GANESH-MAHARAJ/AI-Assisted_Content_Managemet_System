import os
import re
from langchain_ollama import OllamaLLM
from PyPDF2 import PdfReader
from pymongo import MongoClient

def clean_tags(raw_tags):
    cleaned = []
    for line in raw_tags:
        # Remove numbering, bullets, markdown symbols, extra spaces
        line = re.sub(r'^\s*\d+\.\s*', '', line)  # Remove leading numbers + dot + space
        line = re.sub(r'^\s*[\*\-\+]?\s*', '', line)  # Remove bullets (*, -, +)
        line = re.sub(r'(\*\*|__|\*)', '', line)  # Remove markdown bold/italic symbols
        line = line.rstrip(':')  # Remove trailing colon
        line = line.strip()  # Trim whitespace
        
        # Skip empty or irrelevant header lines
        if line and not line.lower().startswith((
            'here are', 'these tags', 'subfields', 'algorithms', 'applications'
        )):
            cleaned.append(line)
    
    # Remove duplicates, keep order
    seen = set()
    cleaned_unique = []
    for tag in cleaned:
        if tag not in seen:
            cleaned_unique.append(tag)
            seen.add(tag)
    return cleaned_unique

def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return None

def store_tags_in_mongo(file_name, content, tags):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client.pdf_tags
        collection = db.tagged_files
        
        document = {
            "file_name": file_name,
            "content": content,
            "tags": tags
        }
        
        collection.insert_one(document)
        print(f"Successfully stored tags for {file_name} in MongoDB.")
    except Exception as e:
        print(f"Error storing tags for {file_name} in MongoDB: {e}")

def generate_tags(file_path):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client.pdf_tags
        collection = db.tagged_files
        
        if collection.find_one({"file_name": file_path}):
            print(f"Record for {file_path} already exists in MongoDB. Skipping processing.")
            return
        
        text = extract_text_from_pdf(file_path)
        if text:
            llm = OllamaLLM(model="llama3.1:latest")
            prompt = f"Generate 100 relevant tags for the following content (Tags must be like, user will be searching tags in search bar and relevent articles will be shown):\n{text[:2000]}"
            response = llm.invoke(prompt)
            
            raw_tags = response.strip().split("\n")
            cleaned_tags = clean_tags(raw_tags)
            
            print(f"Generated cleaned tags for {file_path}: {cleaned_tags}")
            store_tags_in_mongo(file_path, text[:], cleaned_tags)
        else:
            print(f"No text extracted from {file_path}.")
    except Exception as e:
        print(f"Error generating tags for {file_path}: {e}")

def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith(".pdf"):
                file_path = os.path.join(root, file_name)
                print(f"\nProcessing file: {file_path}")
                generate_tags(file_path)

# Change this to your PDFs folder path
folder_path = r"C:\SSPL_CMS\SAMPELproject\arxiv_pdfs"
process_folder(folder_path)
