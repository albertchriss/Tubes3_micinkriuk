import re
import fitz  # PyMuPDF - used for reading PDF files

# --- REGEX PATTERNS ---
# These patterns are used to identify key pieces of information in the resume.
EXPERIENCE_DATE_PATTERN = re.compile(
    r'((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?|0?[1-9]|1[0-2])\s*\'?/?\d{2,4})\s*(?:to|-|–|—)\s*((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?|0?[1-9]|1[0-2])\s*\'?/?\d{2,4}|Present|Current)',
    re.IGNORECASE
)
YEAR_PATTERN = re.compile(r'\b(19[89]\d|20\d{2})\b')
# Removed inline (?i) flags and added more keywords like BBA
EDUCATION_KEYWORDS = r'(B\.S|B\.A|BBA|M\.S|M\.A|Ph\.D|Bachelor|Master|Associate|Diploma|Certificate|High School Diploma)'
INSTITUTION_KEYWORDS = r'(University|College|Institute|School)'
# Expanded the list of section headers based on user feedback to be more comprehensive.
SECTION_HEADERS = r'Work Experience|Employment History|Professional Experience|Relevant Experience|Work History|Internship Experience|Research Experience|Academic Projects|Extracurricular Involvement|Additional Experience|Leadership Experience|Volunteer Experience|Experience|Education|Education and Training|Skills|Technical Skills|Professional Skills|Abilities|Expertise|Competencies|Highlights|Projects|Qualifications|Accomplishments|Awards|Certifications'


class ResumeParser:
    """
    A class to encapsulate the logic for parsing a resume's text.
    It cleans the text, splits it into sections, and extracts structured data.
    """

    def __init__(self, full_text: str):
        """
        Initializes the parser with the full text of the resume.

        Args:
            full_text: A string containing the entire text of the resume.
        """
        self.raw_text = full_text
        self.cleaned_text = self._clean_text(full_text)
        self.sections = self._get_sections()

    def _clean_text(self, text: str) -> str:
        """Removes common PDF artifacts and normalizes whitespace while preserving newlines."""
        if not text:
            return ""
        # Remove common decoding artifacts. Added ï¼ and â€“ from user examples.
        text = re.sub(r'Â|â€|ï¼|â€“', '', text)
        # Normalize HORIZONTAL whitespace (spaces, tabs) to a single space, but leave newlines alone.
        text = re.sub(r'[ \t\xa0]+', ' ', text)
        # Standardize newlines and remove excessive blank lines, preserving paragraph breaks.
        text = re.sub(r'\n\s*\n', '\n\n', text) 
        return text.strip()

    def _get_sections(self) -> dict:
        """Splits the cleaned text into a dictionary of sections by finding headers."""
        sections = {}
        # The title pattern is now much more comprehensive.
        header_pattern = fr'\b({SECTION_HEADERS})\b'
        header_matches = list(re.finditer(header_pattern, self.cleaned_text, re.IGNORECASE))

        if not header_matches:
            sections['Uncategorized'] = self.cleaned_text
            return sections

        # Capture text before the first header
        first_header_start = header_matches[0].start()
        if first_header_start > 0:
            sections['Header'] = self.cleaned_text[:first_header_start].strip()

        # Slice the text between each header
        for i, match in enumerate(header_matches):
            header_text = match.group(1).strip().title()
            content_start = match.end()
            content_end = header_matches[i+1].start() if i + 1 < len(header_matches) else len(self.cleaned_text)
            
            content = self.cleaned_text[content_start:content_end].strip(' :\n')
            sections[header_text] = content
            
        return sections

    def _parse_skills(self) -> list[str]:
        """
        Parses the Skills section into a list of skills, ensuring skills are not long sentences.
        """
        # Added new skill-related headers based on user feedback.
        skills_headers = ['Skills', 'Highlights', 'Technical Skills', 'Professional Skills', 'Abilities', 'Expertise', 'Competencies']
        skills_block = None
        for header in skills_headers:
            skills_block = self.sections.get(header.title())
            if skills_block:
                break

        if not skills_block:
            return []

        # Replace common delimiters with a comma
        cleaned_text = re.sub(r'[\n•*▪|]', ',', skills_block)
        # Split, clean, and filter out empty items
        skills_list = [skill.strip() for skill in cleaned_text.split(',') if skill.strip()]
        
        # Filter out skills that are too long (more than 3 words).
        short_skills = [skill for skill in skills_list if len(skill.split()) <= 3]
        
        # Return a list with duplicates removed while preserving order
        return list(dict.fromkeys(short_skills))

    def _parse_education(self) -> list[dict]:
        """
        Parses the Education section more robustly to handle multiple entries.
        It identifies each entry by looking for patterns that signify a new degree.
        """
        education_block = self.sections.get('Education') or self.sections.get('Education And Training')
        if not education_block:
            return []

        education_list = []
        # Split the block into lines to process them one by one
        lines = education_block.strip().split('\n')
        
        current_entry_lines = []
        # A regex to detect the start of a new educational entry. This can be a year or a degree keyword.
        entry_start_pattern = re.compile(f'({YEAR_PATTERN.pattern}|{EDUCATION_KEYWORDS})', re.IGNORECASE)

        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # If a line looks like the start of a new entry AND there's a current entry being built,
            # process the completed entry first.
            if entry_start_pattern.search(line) and current_entry_lines:
                entry_text = ' '.join(current_entry_lines)
                edu_dict = self._extract_education_details(entry_text)
                if edu_dict:
                    education_list.append(edu_dict)
                # Start a new entry
                current_entry_lines = [line]
            else:
                # Continue building the current entry
                current_entry_lines.append(line)
        
        # Process the last entry in the buffer
        if current_entry_lines:
            entry_text = ' '.join(current_entry_lines)
            edu_dict = self._extract_education_details(entry_text)
            if edu_dict:
                education_list.append(edu_dict)

        return education_list

    def _extract_education_details(self, entry_text: str) -> dict:
        """Helper function to extract details from a single education entry string."""
        edu_dict = {}
        
        # Extract year first, as it's a clear marker
        year_match = YEAR_PATTERN.search(entry_text)
        if year_match:
            edu_dict['year'] = year_match.group(0)
            entry_text = entry_text.replace(year_match.group(0), '').strip()

        # The remaining text likely contains the degree and institution
        parts = [p.strip() for p in re.split(r',|:', entry_text) if p.strip()]

        degree_str = ""
        institution_str = ""
        
        # Find the parts that contain our keywords
        for part in parts:
            if re.search(EDUCATION_KEYWORDS, part, re.IGNORECASE):
                degree_str = part
            elif re.search(INSTITUTION_KEYWORDS, part, re.IGNORECASE):
                institution_str = part
        
        # Assign the found parts
        if degree_str:
            edu_dict['degree'] = degree_str
        if institution_str:
            edu_dict['institution'] = institution_str

        # If we are missing information, try to infer it from the remaining text
        if not edu_dict.get('institution') and edu_dict.get('degree'):
            remaining_text = entry_text.replace(edu_dict['degree'], '').strip(' ,:')
            edu_dict['institution'] = remaining_text
        elif not edu_dict.get('degree') and edu_dict.get('institution'):
            remaining_text = entry_text.replace(edu_dict['institution'], '').strip(' ,:')
            edu_dict['degree'] = remaining_text

        return edu_dict if edu_dict else {}

    def _parse_experience(self) -> list[dict]:
        """
        Parses the Experience section into a list of jobs, matching the requested
        output format: {'position': str, 'description': str, 'year': str}.
        This version iterates through lines to robustly group job entries.
        """
        experience_headers = [
            'Experience', 'Professional Experience', 'Work Experience', 'Work History', 
            'Employment History', 'Relevant Experience', 'Internship Experience', 'Research Experience', 
            'Academic Projects', 'Extracurricular Involvement', 'Additional Experience', 
            'Leadership Experience', 'Volunteer Experience'
        ]
        
        experience_block = None
        for header in experience_headers:
            experience_block = self.sections.get(header.title())
            if experience_block:
                break
        
        if not experience_block:
            return []

        job_entries = []
        current_job_lines = []
        lines = experience_block.strip().split('\n')

        for line in lines:
            # A new job entry is identified by a line containing a date pattern.
            is_new_job_header = EXPERIENCE_DATE_PATTERN.search(line) and not line.strip().startswith(('•', '*', '-'))
            
            if is_new_job_header and current_job_lines:
                # If we find a new job header and we have lines for a previous job,
                # process the previous job entry.
                job_entries.append("\n".join(current_job_lines))
                current_job_lines = [line]  # Start the new job entry
            else:
                # Otherwise, keep adding lines to the current job entry.
                current_job_lines.append(line)
        
        # Add the last job entry from the buffer
        if current_job_lines:
            job_entries.append("\n".join(current_job_lines))

        job_list = []
        for entry_text in job_entries:
            if not entry_text:
                continue

            entry_lines = [ln.strip() for ln in entry_text.split('\n') if ln.strip()]
            if not entry_lines:
                continue

            # First line has the position and year
            first_line = entry_lines[0]
            date_match = EXPERIENCE_DATE_PATTERN.search(first_line)
            
            position = first_line
            year = ""
            if date_match:
                position = first_line[:date_match.start()].strip(' ,')
                year = date_match.group(0)

            # Second line is likely the company, which will be the description
            company = ''
            if len(entry_lines) > 1 and not entry_lines[1].startswith(('•', '*', '-')):
                company = entry_lines[1]

            # Clean up placeholders
            position = re.sub(r',?\s*Company Name', '', position, flags=re.IGNORECASE).strip(' ,')
            company = re.sub(r'Company Name', '', company, flags=re.IGNORECASE).strip(' ,')

            if position:
                job_list.append({
                    'position': position,
                    'description': company, # Company name goes into the description field
                    'year': year
                })

        return job_list


    def parse(self) -> dict:
        """
        Orchestrates the parsing of all sections and returns the final structured data.
        The key 'job_history' is used for compatibility with the original code.
        """
        return {
            "skills": self._parse_skills(),
            "education": self._parse_education(),
            "job_history": self._parse_experience(),
        }


def process_cv(full_text: str) -> dict:
    """
    Main function to process the full text of a resume. It preserves the original
    input/output signature while using the improved ResumeParser class internally.

    Args:
        full_text: A string containing the entire text of the resume.

    Returns:
        A dictionary with the parsed data structured into 'skills', 'education', and 'job_history'.
    """
    if not isinstance(full_text, str) or not full_text:
        return {"skills": [], "education": [], "job_history": []}
        
    parser = ResumeParser(full_text)
    return parser.parse()

# --- Example Usage ---
#
# def extract_text_from_pdf(pdf_path):
#     """Extracts all text from a given PDF file."""
#     try:
#         doc = fitz.open(pdf_path)
#         text = "".join(page.get_text("text") for page in doc)
#         doc.close()
#         return text
#     except Exception as e:
#         print(f"Error reading PDF {pdf_path}: {e}")
#         return ""
#
# if __name__ == '__main__':
#     # Make sure to place the PDF files in the same directory or provide full paths
#     resume_files = ['15603319.pdf', '12341902.pdf', '16661264.pdf']
#
#     for resume_file in resume_files:
#         print(f"\n--- Processing Resume: {resume_file} ---")
#         resume_text = extract_text_from_pdf(resume_file)
#
#         if resume_text:
#             parsed_data = process_cv(resume_text)
#             import json
#             print(json.dumps(parsed_data, indent=2))
#         else:
#             print("Could not extract text from the PDF.")
