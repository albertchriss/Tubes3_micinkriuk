import re
import fitz  # PyMuPDF - used for reading PDF files

# --- REGEX PATTERNS ---
# These patterns are used to identify key pieces of information in the resume.
EXPERIENCE_DATE_PATTERN = re.compile(
    r'((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?|0?[1-9]|1[0-2])\s*\'?/?\d{2,4})\s*(?:to|-|–|—)\s*((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?|0?[1-9]|1[0-2])\s*\'?/?\d{2,4}|Present|Current)',
    re.IGNORECASE
)
YEAR_PATTERN = re.compile(r'\b(19[89]\d|20\d{2})\b')
EDUCATION_KEYWORDS = r'(?i)(B\.S|B\.A|M\.S|M\.A|Ph\.D|Bachelor|Master|Associate|Diploma|Certificate|High School Diploma)'
INSTITUTION_KEYWORDS = r'(?i)(University|College|Institute|School)'
SECTION_HEADERS = r'Experience|Professional Experience|Work Experience|Education|Education and Training|Skills|Highlights|Projects|Qualifications|Accomplishments|Awards|Certifications'


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
        """Removes common PDF artifacts and normalizes whitespace."""
        if not text:
            return ""
        text = re.sub(r'[\s\xa0]+', ' ', text)  # Normalize whitespace and remove non-breaking spaces
        text = re.sub(r'Â|â€', '', text)  # Remove common decoding artifacts
        text = re.sub(r'1/4|i¼', '', text) # Remove other artifacts
        return text.strip()

    def _get_sections(self) -> dict:
        """Splits the cleaned text into a dictionary of sections by finding headers."""
        # This new method finds headers without relying on specific newline patterns, making it more robust.
        sections = {}
        # Find the start index of all headers using word boundaries (\b)
        header_matches = list(re.finditer(fr'\b({SECTION_HEADERS})\b', self.cleaned_text, re.IGNORECASE))

        if not header_matches:
            sections['Uncategorized'] = self.cleaned_text
            return sections

        # Capture the text before the very first header
        first_header_start = header_matches[0].start()
        if first_header_start > 0:
            sections['Header'] = self.cleaned_text[:first_header_start].strip()

        # Slice the text between each header to get the content for that section
        for i, match in enumerate(header_matches):
            header_text = match.group(1).strip().title()
            content_start = match.end()
            content_end = header_matches[i+1].start() if i + 1 < len(header_matches) else len(self.cleaned_text)
            
            # Clean up content, removing leading colons or whitespace
            content = re.sub(r'^[:\s]*', '', self.cleaned_text[content_start:content_end]).strip()
            sections[header_text] = content
            
        return sections

    def _parse_skills(self) -> list[str]:
        """Parses the Skills or Highlights section into a list of skills."""
        skills_block = self.sections.get('Skills') or self.sections.get('Highlights')
        if not skills_block:
            return []

        # Replace common delimiters with a comma
        cleaned_text = re.sub(r'[\n•*▪|]', ',', skills_block)
        # Split, clean, and filter out empty items
        skills_list = [skill.strip() for skill in cleaned_text.split(',') if len(skill.strip()) > 2]
        # Return a list with duplicates removed while preserving order
        return list(dict.fromkeys(skills_list))

    def _parse_education(self) -> list[dict]:
        """Parses the Education section into a list of educational experiences."""
        education_block = self.sections.get('Education') or self.sections.get('Education And Training')
        if not education_block:
            return []

        # Split the block into entries based on blank lines, a common separator.
        entries = re.split(r'\n\s*\n', education_block)
        education_list = []
        for entry in entries:
            if len(entry.strip()) < 5:
                continue
            
            edu_dict = {}
            # Extract year, degree, and institution from each entry
            year_match = YEAR_PATTERN.search(entry)
            if year_match:
                edu_dict['year'] = year_match.group(0)

            # Find the line containing a degree keyword
            for line in entry.split('\n'):
                if re.search(EDUCATION_KEYWORDS, line, re.IGNORECASE):
                    edu_dict['degree'] = line.strip()
                    break

            # Find the line containing an institution keyword
            for line in entry.split('\n'):
                if re.search(INSTITUTION_KEYWORDS, line, re.IGNORECASE):
                    edu_dict['institution'] = line.strip()
                    break
            
            if edu_dict:
                education_list.append(edu_dict)
        return education_list

    def _parse_experience(self) -> list[dict]:
        """Parses the Experience section into a list of jobs."""
        experience_block = self.sections.get('Experience') or self.sections.get('Professional Experience') or self.sections.get('Work Experience')
        if not experience_block:
            return []

        job_entries = []
        # Find all date ranges, which act as reliable anchors for job entries.
        date_matches = list(EXPERIENCE_DATE_PATTERN.finditer(experience_block))
        if not date_matches:
            # Fallback for when dates are not found: split by blank lines
            return [{'description': entry} for entry in re.split(r'\n\s*\n', experience_block) if entry.strip()]

        # Assume the text between two dates belongs to the first one.
        start_pos = 0
        for i, match in enumerate(date_matches):
            # This logic is complex. A simpler split by blank lines is often more reliable.
            # We will use that as the primary strategy.
            pass # Keep date_matches for internal parsing but don't use for splitting the block.
            
        entries = re.split(r'\n\s*\n', experience_block)
        job_list = []
        for entry in entries:
            if not entry or len(entry) < 20:
                continue

            job_dict = {}
            # Extract the date from the entry
            date_match = EXPERIENCE_DATE_PATTERN.search(entry)
            if date_match:
                job_dict['dates'] = date_match.group(0)
                entry = entry.replace(date_match.group(0), '')
            else:
                job_dict['dates'] = ''

            lines = [line.strip() for line in entry.split('\n') if line.strip()]
            if not lines:
                continue

            # Heuristic: First line is position, second is company.
            job_dict['position'] = lines[0]
            job_dict['company'] = lines[1] if len(lines) > 1 and not EXPERIENCE_DATE_PATTERN.search(lines[1]) else ''
            # The rest is the description.
            desc_start_index = 2 if job_dict['company'] else 1
            job_dict['description'] = ' '.join(lines[desc_start_index:]).strip()
            job_list.append(job_dict)

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
    # Handle empty or invalid input gracefully.
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
#         text = "".join(page.get_text() for page in doc)
#         doc.close()
#         return text
#     except Exception as e:
#         print(f"Error reading PDF {pdf_path}: {e}")
#         return ""
#
# if __name__ == '__main__':
#     resume_files = ['16849128.pdf'] # Add your PDF file paths here
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
