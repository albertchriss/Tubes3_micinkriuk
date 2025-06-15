import pypdf

def extract_text_from_pdf(pdf_path):
    text = ""
    print(f"Extracting text from {pdf_path}...")
    try:
        with open(pdf_path, "rb") as file:
            reader = pypdf.PdfReader(file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
    
    return text