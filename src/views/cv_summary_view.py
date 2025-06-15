import flet as ft
from components.cv_personal_info import CVPersonalInfo
from components.cv_skills import CVSkills
from components.cv_education import CVEducation
from components.cv_job_history import CVJobHistory

def cv_summary_view(page: ft.Page, cv_data):
    """
    Create CV Summary view
    cv_data should contain: name, birthdate, address, phone, skills, education, job_history
    """
    # Debug: Print the CV data to see what we're getting
    print(f"CV Summary - Received data: {cv_data}")

    # Set default values if cv_data is None or empty
    if not cv_data:
        cv_data = {
            "name": "No Data",
            "birthdate": "N/A",
            "address": "N/A", 
            "phone": "N/A",
            "skills": [],
            "education": [],
            "job_history": []
        }
        
    def go_back(e):
        # Navigate back to search results
        page.go("/")
    
    # Create component instances
    personal_info = CVPersonalInfo(cv_data)
    skills = CVSkills(cv_data)
    education = CVEducation(cv_data)
    job_history = CVJobHistory(cv_data)
    
    return ft.Container(
        content=ft.Column([
            # Header with back button
            ft.Container(
                content=ft.Row([
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=go_back,
                            icon_color="#4A90E2"
                        ),
                        ft.Text("Back to Search", size=14, color="#4A90E2"),
                    ], spacing=5),
                    ft.Text("CV Summary", size=20, weight=ft.FontWeight.BOLD, color="#4A90E2")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.all(20),
                bgcolor="#FFFFFF",
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color="#1A000000",
                    offset=ft.Offset(0, 2)
                ),
            ),
            
            # Personal info component
            personal_info.container,
            
            # Skills and Education in the same row
            ft.Container(
                content=ft.Row([
                    skills.container,
                    education.container
                ], spacing=15),
                padding=ft.padding.symmetric(horizontal=20, vertical=10)
            ),
            
            # Job History - full width with proper margins
            ft.Container(
                content=job_history.container,
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                width=float('inf')  # Ensure full width
            ),
            
            # View Full CV button
            ft.Container(
                content=ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.VISIBILITY, color="#FFFFFF"),
                        ft.Text("View Full CV", color="#FFFFFF", size=16)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    bgcolor="#4A90E2",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.padding.symmetric(horizontal=40, vertical=15)
                    )
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.all(20)
            )
        ], spacing=0, scroll=ft.ScrollMode.AUTO),
        alignment=ft.alignment.top_center,
        padding=0,
        expand=True,
        bgcolor="#F5F5F5",  # Same background color as home page
    )