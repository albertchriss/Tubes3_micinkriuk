import flet as ft
import webbrowser
from pathlib import Path
from core.service import get_cv_data_by_detail_id

# def get_cv_data_by_detail_id(applicant_id):
#     """
#     Dummy function to simulate fetching CV data by applicant ID
#     Returns different CV data based on applicant_id
#     """
#     dummy_data = {
#         1: {
#             "name": "Farhan Abdullah",
#             "birthdate": "15-03-1995",
#             "address": "Jalan Sariasih Sarijadi ITB",
#             "phone": "0812-3456-7890",
#             "skills": ["JavaScript", "React", "Node.js", "Express", "HTML", "CSS", "MongoDB"],
#             "education": [
#                 {
#                     "degree": "Informatics Engineering",
#                     "institution": "Institut Teknologi Bandung",
#                     "year": "2022-2026"
#                 }
#             ],
#             "job_history": [
#                 {
#                     "position": "CTO",
#                     "description": "Leading the organization's technology strategies",
#                     "year": "2000-2004"
#                 },
#                 {
#                     "position": "Senior Developer",
#                     "description": "Developing and maintaining web applications",
#                     "year": "1998-2000"
#                 }
#             ]
#         },
#         2: {
#             "name": "Sarah Johnson",
#             "birthdate": "22-07-1993",
#             "address": "Jalan Dipatiukur No. 35 Bandung",
#             "phone": "0813-9876-5432",
#             "skills": ["Python", "Django", "PostgreSQL", "Docker", "AWS", "REST API"],
#             "education": [
#                 {
#                     "degree": "Computer Science",
#                     "institution": "Universitas Padjadjaran",
#                     "year": "2018-2022"
#                 }
#             ],
#             "job_history": [
#                 {
#                     "position": "Backend Developer",
#                     "description": "Developing scalable backend systems using Python and Django",
#                     "year": "2022-2024"
#                 },
#                 {
#                     "position": "Junior Developer",
#                     "description": "Building web applications and APIs",
#                     "year": "2020-2022"
#                 }
#             ]
#         },
#         3: {
#             "name": "Ahmad Rizky",
#             "birthdate": "10-11-1994",
#             "address": "Jalan Gegerkalong Hilir Bandung",
#             "phone": "0814-1234-5678",
#             "skills": ["Java", "Spring Boot", "MySQL", "Kubernetes", "Jenkins", "Git"],
#             "education": [
#                 {
#                     "degree": "Software Engineering",
#                     "institution": "Universitas Telkom",
#                     "year": "2016-2020"
#                 },
#                 {
#                     "degree": "AWS Certified Developer",
#                     "institution": "Amazon Web Services",
#                     "year": "2023"
#                 }
#             ],
#             "job_history": [
#                 {
#                     "position": "DevOps Engineer",
#                     "description": "Managing CI/CD pipelines and cloud infrastructure",
#                     "year": "2023-2024"
#                 },
#                 {
#                     "position": "Full Stack Developer",
#                     "description": "Developing enterprise applications using Java Spring Boot",
#                     "year": "2020-2023"
#                 }
#             ]
#         },
#         4: {
#             "name": "Lisa Chen",
#             "birthdate": "05-09-1996",
#             "address": "Jalan Dago Pojok Bandung",
#             "phone": "0815-5555-1234",
#             "skills": ["Flutter", "Dart", "Firebase", "Android", "iOS", "React Native"],
#             "education": [
#                 {
#                     "degree": "Information Systems",
#                     "institution": "Universitas Kristen Maranatha",
#                     "year": "2019-2023"
#                 }
#             ],
#             "job_history": [
#                 {
#                     "position": "Mobile Developer",
#                     "description": "Creating cross-platform mobile applications using Flutter",
#                     "year": "2023-2024"
#                 },
#                 {
#                     "position": "Mobile App Intern",
#                     "description": "Learning mobile development and contributing to projects",
#                     "year": "2022-2023"
#                 }
#             ]
#         },
#         5: {
#             "name": "David Wilson",
#             "birthdate": "18-12-1992",
#             "address": "Jalan Setiabudi Bandung",
#             "phone": "0816-7777-8888",
#             "skills": ["C#", ".NET", "SQL Server", "Azure", "Entity Framework", "ASP.NET"],
#             "education": [
#                 {
#                     "degree": "Information Technology",
#                     "institution": "Universitas Widyatama",
#                     "year": "2014-2018"
#                 },
#                 {
#                     "degree": "Microsoft Certified Developer",
#                     "institution": "Microsoft",
#                     "year": "2021"
#                 }
#             ],
#             "job_history": [
#                 {
#                     "position": "Senior .NET Developer",
#                     "description": "Leading .NET development team and architecting solutions",
#                     "year": "2021-2024"
#                 },
#                 {
#                     "position": ".NET Developer",
#                     "description": "Developing enterprise applications using .NET framework",
#                     "year": "2018-2021"
#                 },
#                 {
#                     "position": "Senior .NET Developer",
#                     "description": "Leading .NET development team and architecting solutions",
#                     "year": "2021-2024"
#                 },
#                 {
#                     "position": ".NET Developer",
#                     "description": "Developing enterprise applications using .NET framework",
#                     "year": "2018-2021"
#                 }
#             ]
#         }
#     }
    
#     return dummy_data.get(applicant_id, {
#         "name": "Unknown Applicant",
#         "birthdate": "N/A",
#         "address": "N/A",
#         "phone": "N/A",
#         "skills": [],
#         "education": [],
#         "job_history": []
#     })

class ResultCard:
    def __init__(self, applicant_id, detail_id, name, matched_keywords, keywords_data, cv_path, bgcolor="#E3F2FD", on_summary_click=None):
        self.applicant_id = applicant_id
        self.name = name
        self.matched_keywords = matched_keywords
        self.keywords_data = keywords_data
        self.cv_path = cv_path
        self.bgcolor = bgcolor
        self.on_summary_click = on_summary_click
        self.detail_id = detail_id
        
        self.container = self._create_card()
    
    def _on_summary_clicked(self, e):
        """Handle summary button click - fetch CV data and call callback"""
        print(f"Summary clicked for applicant ID: {self.applicant_id}")
        
        # Fetch CV data using applicant_id
        # TODO: Implement get_cv_data_by_applicant_id
        cv_data = get_cv_data_by_detail_id(self.detail_id) 
        
        if cv_data and self.on_summary_click:
            self.on_summary_click(cv_data, self.cv_path)
        else:
            print(f"Could not fetch CV data for applicant {self.applicant_id}")
    
    def _on_view_cv_clicked(self, e):
        """Handle View CV button click - open PDF in default browser"""
        print(f"View CV clicked for applicant ID: {self.applicant_id}")
        
        if not self.cv_path:
            print("No CV path provided")
            return
        
        try:
            # Convert to Path object for better handling
            cv_path = Path(self.cv_path)
            
            # Check if file exists
            if not cv_path.exists():
                print(f"CV file not found: {cv_path}")
                return
            
            # Get absolute path and open in browser
            absolute_path = cv_path.resolve()
            webbrowser.open(f"file:///{absolute_path}")
            print(f"Opening PDF in browser: {absolute_path}")
            
        except Exception as ex:
            print(f"Error opening CV file: {ex}")
            
    def _create_card(self):
        """Create the CV card container"""
        
        keyword_widgets = []
        for i, keyword_data in enumerate(self.keywords_data, 1):
            keyword_widgets.append(
                ft.Row([
                    ft.Text(f"{i}. {keyword_data['keyword']}:", size=14, color="#000000", expand=True),
                    ft.Container(
                        content=ft.Text(f"{keyword_data['occurrences']} occurrence{'s' if keyword_data['occurrences'] != 1 else ''}", 
                                       size=12, color="#FFFFFF"),
                        bgcolor="#4A90E2",
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=15
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )
        
        keywords_section = ft.Container(
            content=ft.Column(
                controls=keyword_widgets,
                spacing=5,
                scroll=ft.ScrollMode.HIDDEN if len(keyword_widgets) > 3 else None
            ),
            height=105,
            padding=ft.padding.symmetric(vertical=5),
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text(self.name, size=20, weight=ft.FontWeight.BOLD, color="#424242"),
                ft.Text(f"{self.matched_keywords} matched keyword{'s' if self.matched_keywords != 1 else ''}", 
                        size=14, color="#666666"),
                
                ft.Container(height=10),
                keywords_section,
                ft.Container(height=15),
                
                ft.Row([
                    ft.OutlinedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.DESCRIPTION, size=16, color="#4A90E2"),
                            ft.Text("Summary", color="#4A90E2", size=14)
                        ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                        style=ft.ButtonStyle(
                            side=ft.BorderSide(1, "#4A90E2"),
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.symmetric(horizontal=16, vertical=8)
                        ),
                        expand=True,
                        on_click=self._on_summary_clicked
                    ),
                    ft.OutlinedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.VISIBILITY, size=16, color="#9C27B0"),
                            ft.Text("View CV", color="#9C27B0", size=14)
                        ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                        style=ft.ButtonStyle(
                            side=ft.BorderSide(1, "#9C27B0"),
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.symmetric(horizontal=16, vertical=8)
                        ),
                        expand=True,
                        on_click=self._on_view_cv_clicked
                    ),
                ], spacing=15)
            ], spacing=5),
            padding=ft.padding.all(20),
            bgcolor=self.bgcolor,
            border_radius=12,
            border=ft.border.all(1, "#D0D0D0"),
            expand=True
        )