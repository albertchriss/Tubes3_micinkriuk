import fitz 

def extract_text_from_pdf(pdf_path):
    text = ""
    print(f"Mengekstrak teks dari {pdf_path}...")
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text() + "\n"
        return text
    except Exception as e:
        print(f"Error saat mengekstrak teks dari {pdf_path}: {e}")
        return None