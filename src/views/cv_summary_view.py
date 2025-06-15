from pathlib import Path
import webbrowser
import flet as ft
from components.cv_personal_info import CVPersonalInfo
from components.cv_skills import CVSkills
from components.cv_education import CVEducation
from components.cv_job_history import CVJobHistory

def cv_summary_view(page: ft.Page, cv_data, cv_path):
    """
    Create CV Summary view
    cv_data should contain: name, birthdate, address, phone, skills, education, job_history
    """
    print(f"CV Summary - Received data: {cv_data}")

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
        page.go("/")
    
    def view_full_cv(e):
        """Handle View CV button click - open PDF in default browser"""
        
        if not cv_path:
            print("No CV path provided")
            return
        
        try:
            # Convert to Path object for better handling
            cv_file_path = Path(cv_path)
            
            # Check if file exists
            if not cv_file_path.exists():
                print(f"CV file not found: {cv_file_path}")
                return
            
            # Get absolute path and open in browser
            absolute_path = cv_file_path.resolve()
            webbrowser.open(f"file:///{absolute_path}")
            print(f"Opening PDF in browser: {absolute_path}")
            
        except Exception as ex:
            print(f"Error opening CV file: {ex}")
    personal_info = CVPersonalInfo(cv_data)
    skills = CVSkills(cv_data)
    education = CVEducation(cv_data)
    job_history = CVJobHistory(cv_data)
    
    return ft.Container(
        content=ft.Column([
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
            
            personal_info.container,
            
            ft.Container(
                content=ft.Row([
                    skills.container,
                    education.container
                ], spacing=15),
                padding=ft.padding.symmetric(horizontal=20, vertical=10)
            ),
            
            ft.Container(
                content=job_history.container,
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                width=float('inf') 
            ),
            
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
                    ),
                    on_click=view_full_cv
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.all(20)
            )
        ], spacing=0, scroll=ft.ScrollMode.AUTO),
        alignment=ft.alignment.top_center,
        padding=0,
        expand=True,
        bgcolor="#F5F5F5",
    )