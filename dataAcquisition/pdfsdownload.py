import requests
import xml.etree.ElementTree as ET
import time
import os

# Create folder for PDFs
os.makedirs('arxiv_pdfs', exist_ok=True)

base_api_url = 'http://export.arxiv.org/api/query?'

# List of categories to download from
categories = [
    'cs.AI',       # Artificial Intelligence
    'cs.LG',       # Machine Learning
    'stat.ML',     # Statistics - Machine Learning
    'math.OC',     # Optimization and Control
    'physics.data-an'  # Data Analysis, Statistics and Probability
]

max_papers_per_cat = 200  # To keep total around 1000 (5 categories * 200 = 1000)
batch_size = 50           # Number of papers per API request

for category in categories:
    print(f'\n=== Starting downloads for category: {category} ===\n')
    start = 0
    total_downloaded = 0

    while total_downloaded < max_papers_per_cat:
        print(f'Fetching papers {start + 1} to {start + batch_size} in {category}')
        url = f'{base_api_url}search_query=cat:{category}&start={start}&max_results={batch_size}'
        response = requests.get(url)
        root = ET.fromstring(response.content)

        entries = root.findall('{http://www.w3.org/2005/Atom}entry')

        if not entries:
            print(f'No more papers found for category {category}')
            break

        for entry in entries:
            id_url = entry.find('{http://www.w3.org/2005/Atom}id').text
            paper_id = id_url.split('/abs/')[-1]
            pdf_url = f'https://arxiv.org/pdf/{paper_id}.pdf'

            filename = f'arxiv_pdfs/{paper_id.replace("/", "_")}.pdf'
            if os.path.exists(filename):
                print(f'Already downloaded {filename}, skipping.')
                continue

            print(f'Downloading {pdf_url}')
            pdf_response = requests.get(pdf_url)

            if pdf_response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(pdf_response.content)
                print(f'Saved: {filename}')
                total_downloaded += 1
            else:
                print(f'Failed to download {pdf_url}')
            time.sleep(1)  # Be polite

            if total_downloaded >= max_papers_per_cat:
                break

        start += batch_size

print('\nAll downloads complete.')
