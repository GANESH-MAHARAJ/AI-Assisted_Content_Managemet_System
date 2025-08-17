import os
from PyPDF2 import PdfReader
from pymongo import MongoClient

def extract_full_text(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return None

def update_content_only(folder_path):
    client = MongoClient("mongodb://localhost:27017/")
    db = client.pdf_tags
    collection = db.tagged_files

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith(".pdf"):
                file_path = os.path.join(root, file_name)
                file_path = os.path.abspath(file_path)
                print(f"Processing: {file_path}")

                doc = collection.find_one({"file_name": file_path})
                if doc:
                    full_text = extract_full_text(file_path)
                    if full_text:
                        collection.update_one(
                            {"_id": doc["_id"]},
                            {"$set": {"content": full_text}}
                        )
                        print("Updated content field.")
                    else:
                        print("No text extracted from PDF.")
                else:
                    print("Document not found in DB. Skipping.")

if __name__ == "__main__":
    folder_path = r"C:\\SSPL_CMS\\SAMPELproject\\arxiv_pdfs"
    update_content_only(folder_path)
