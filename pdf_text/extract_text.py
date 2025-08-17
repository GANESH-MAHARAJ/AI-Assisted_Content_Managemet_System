import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)  # Open the PDF file
        text = ""
        for page_num, page in enumerate(doc, start=1):
            page_text = page.get_text()
            text += f"Page {page_num}:\n{page_text}\n"
        doc.close()
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

text = extract_text_from_pdf(r"C:\SSPL_CMS\SAMPELproject\arxiv_pdfs\0704.1274v1.pdf")
print(len(text))
