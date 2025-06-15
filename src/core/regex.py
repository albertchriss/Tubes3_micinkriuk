import fitz  # PyMuPDF
import re

def extract_text_with_pymupdf(pdf_path):
    """Mengekstrak seluruh teks dari file PDF menggunakan PyMuPDF (fitz)."""
    text = ""
    print(f"Mengekstrak teks dari {pdf_path} menggunakan PyMuPDF...")
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text() + "\n" # type: ignore
        return text
    except Exception as e:
        print(f"Error saat mengekstrak teks dari {pdf_path}: {e}")
        return None

def parse_skills(skills_block):
    """Mem-parsing blok teks skills menjadi sebuah list yang lebih bersih."""
    if not skills_block:
        return []
    
    # Hapus judul bagian seperti 'Skills' atau 'Highlights' dari blok itu sendiri
    skills_block = re.sub(r'(?i)skills|highlights', '', skills_block)
    # Ganti baris baru dan bullet dengan koma
    cleaned_text = re.sub(r'[\n•*-]', ',', skills_block)
    
    # Pisahkan, bersihkan, dan hapus item yang tidak relevan/kosong
    skills_list = [skill.strip() for skill in cleaned_text.split(',') if len(skill.strip()) > 1]
    return skills_list

def parse_education(education_block):
    """Mem-parsing blok teks education dengan logika yang lebih baik."""
    if not education_block:
        return []
        
    education_list = []
    # Pola untuk mengenali baris yang memulai entri pendidikan
    entry_pattern = r'(?i)(bachelor|master|associate|phd|diploma|b\.s|m\.s|b\.a)'
    
    current_entry_lines = []
    for line in education_block.strip().split('\n'):
        if re.search(entry_pattern, line) and current_entry_lines:
            entry_text = ' '.join(current_entry_lines)
            edu_dict = {}
            year_match = re.search(r'(\d{4})', entry_text)
            if year_match:
                edu_dict['year'] = year_match.group(1)
            
            # Sisa teks adalah gelar dan institusi
            degree_text = entry_text.replace(edu_dict.get('year', ''), '').strip()
            parts = degree_text.split(',')
            edu_dict['degree'] = parts[0].strip()
            edu_dict['institution'] = ','.join(parts[1:]).strip() if len(parts) > 1 else ''

            education_list.append(edu_dict)
            current_entry_lines = [line] 
        else:
            current_entry_lines.append(line)
            
    # Proses entri terakhir yang tersisa
    if current_entry_lines:
        entry_text = ' '.join(current_entry_lines)
        edu_dict = {}
        year_match = re.search(r'(\d{4})', entry_text)
        if year_match:
            edu_dict['year'] = year_match.group(1)
        
        degree_text = entry_text.replace(edu_dict.get('year', ''), '').strip()
        parts = degree_text.split(',')
        edu_dict['degree'] = parts[0].strip()
        edu_dict['institution'] = ','.join(parts[1:]).strip() if len(parts) > 1 else ''
        education_list.append(edu_dict)
        
    return education_list

def parse_experience(experience_block):
    """Mem-parsing blok teks experience dengan pemisah entri yang lebih cerdas."""
    if not experience_block:
        return []

    splitter_pattern = r'\n(?=[A-Z][a-z\s]+.*\n(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4})'
    entries = re.split(splitter_pattern, experience_block.strip())
    
    job_list = []
    year_pattern = r'(?i)((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{4}\s*to\s*(?:Current|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{4}))'

    for entry in entries:
        if not entry.strip() or len(entry.strip()) < 20: # Abaikan entri yang terlalu pendek
            continue
            
        lines = [line.strip() for line in entry.split('\n') if line.strip()]
        job_dict = {}
        
        job_dict['position'] = lines[0]
        
        year_match = re.search(year_pattern, entry)
        job_dict['year'] = year_match.group(0) if year_match else ''
        
        # Gabungkan semua baris menjadi satu untuk deskripsi
        full_desc_text = ' '.join(lines[1:])
        # Hapus info tahun dari deskripsi
        if job_dict['year']:
            full_desc_text = full_desc_text.replace(job_dict['year'], '')
        job_dict['description'] = re.sub(r'\s+', ' ', full_desc_text).strip()
        
        job_list.append(job_dict)

    return job_list

def process_cv(full_text):

    # Pola Regex untuk Ekstraksi Blok (termasuk 'Highlights' untuk skills)
    pattern_experience = r"(?i)(?:Experience|Professional Experience|Work Experience)\b([\s\S]*?)(?=\n(?:Education|Skills|Highlights|Projects|Qualifications|Accomplishments|Awards)\b|\Z)"
    pattern_education = r"(?i)(?:Education|Education and Training)\b([\s\S]*?)(?=\n(?:Experience|Skills|Highlights|Projects|Qualifications|Accomplishments|Awards)\b|\Z)"
    pattern_skills = r"(?i)(?:Skills|Highlights)\b([\s\S]*?)(?=\n(?:Experience|Education|Projects|Qualifications|Accomplishments|Awards)\b|\Z)"

    # Ekstrak setiap blok
    experience_block_match = re.search(pattern_experience, full_text)
    education_block_match = re.search(pattern_education, full_text)
    skills_block_match = re.search(pattern_skills, full_text)

    # Parsing setiap blok
    skills = parse_skills(skills_block_match.group(1) if skills_block_match else None)
    education = parse_education(education_block_match.group(1) if education_block_match else None)
    job_history = parse_experience(experience_block_match.group(1) if experience_block_match else None)

    cv_data = {
        "skills": skills,
        "education": education,
        "job_history": job_history
    }
    
    return cv_data