import flet as ft

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
    
    # Personal info section
    personal_info = ft.Row([
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.CALENDAR_MONTH, color="#4A90E2", size=16),
                ft.Text(f"Birthdate: {cv_data.get('birthdate', 'DD-MM-YYYY')}", size=14)
            ], spacing=8),
            bgcolor="#E3F2FD",
            padding=ft.padding.all(15),
            border_radius=8,
            expand=True
        ),
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.LOCATION_ON, color="#9C27B0", size=16),
                ft.Text(f"Address: {cv_data.get('address', 'N/A')}", size=14)
            ], spacing=8),
            bgcolor="#F3E5F5",
            padding=ft.padding.all(15),
            border_radius=8,
            expand=True
        ),
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.PHONE, color="#4A90E2", size=16),
                ft.Text(f"Phone: {cv_data.get('phone', 'N/A')}", size=14)
            ], spacing=8),
            bgcolor="#E3F2FD",
            padding=ft.padding.all(15),
            border_radius=8,
            expand=True
        ),
    ], spacing=15)
    
    # Skills section
    skills_chips = []
    for skill in cv_data.get('skills', []):
        skills_chips.append(
            ft.Container(
                content=ft.Text(skill, size=12, color="#FFFFFF"),
                bgcolor="#4A90E2",
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=15,
                margin=ft.margin.only(right=8, bottom=8)
            )
        )
    
    skills_section = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text("Skills", size=18, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                padding=ft.padding.all(20),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.center_left,
                    end=ft.alignment.center_right,
                    colors=["#9C27B0", "#4A90E2"]
                ),
                width=float('inf'),
            ),
            ft.Container(
                content=ft.Column([
                    ft.Row(skills_chips[:4], wrap=True) if len(skills_chips) > 4 else ft.Row(skills_chips, wrap=True),
                    ft.Row(skills_chips[4:], wrap=True) if len(skills_chips) > 4 else ft.Container()
                ]),
                padding=ft.padding.all(20),
                bgcolor="#FFFFFF"
            )
        ]),
        border_radius=10,
        expand=True
    )
    
    # Education section
    education_items = []
    for edu in cv_data.get('education', []):
        education_items.append(
            ft.Container(
                content=ft.Column([
                    ft.Text(edu.get('degree', 'N/A'), size=16, weight=ft.FontWeight.BOLD, color="#4A90E2"),
                    ft.Text(edu.get('institution', 'N/A'), size=14, color="#666666"),
                    ft.Text(edu.get('year', 'N/A'), size=12, color="#999999")
                ], spacing=2),
                padding=ft.padding.all(15),
                bgcolor="#F8F9FA",
                border_radius=8,
                border=ft.border.only(left=ft.BorderSide(4, "#4A90E2"))
            )
        )
    
    education_section = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text("Education", size=18, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                padding=ft.padding.all(20),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.center_left,
                    end=ft.alignment.center_right,
                    colors=["#4A90E2", "#50E3C2"]
                ),
                width=float('inf'),
            ),
            ft.Container(
                content=ft.Column(education_items, spacing=10),
                padding=ft.padding.all(20),
                bgcolor="#FFFFFF"
            )
        ]),
        border_radius=10,
        expand=True
    )
    
    # Job History section
    job_items = []
    for job in cv_data.get('job_history', []):
        job_items.append(
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Text(job.get('position', 'N/A'), size=16, weight=ft.FontWeight.BOLD, color="#4A90E2"),
                            ft.Text(job.get('description', 'N/A'), size=14, color="#666666")
                        ], expand=True),
                        ft.Container(
                            content=ft.Text(job.get('year', 'N/A'), size=12, color="#FFFFFF"),
                            bgcolor="#9C27B0",
                            padding=ft.padding.symmetric(horizontal=12, vertical=6),
                            border_radius=15
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ], spacing=5),
                padding=ft.padding.all(15),
                bgcolor="#F8F9FA",
                border_radius=8,
                border=ft.border.only(left=ft.BorderSide(4, "#4A90E2"))
            )
        )
    
    job_history_section = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text("Job History", size=18, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                padding=ft.padding.all(20),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.center_left,
                    end=ft.alignment.center_right,
                    colors=["#4A90E2", "#9C27B0"]
                ),
                width=float('inf'),
            ),
            ft.Container(
                content=ft.Column(job_items, spacing=10),
                padding=ft.padding.all(20),
                bgcolor="#FFFFFF"
            )
        ]),
        border_radius=10,
    )
    
    return ft.ListView(
        controls=[
            # Header with back button
            ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        on_click=go_back,
                        icon_color="#4A90E2"
                    ),
                    ft.Text("Back to Search", size=14, color="#4A90E2"),
                    ft.Container(expand=True),
                    ft.Text("CV Summary", size=20, weight=ft.FontWeight.BOLD, color="#4A90E2")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.all(20),
                bgcolor="#F5F5F5"
            ),
            
            # Name header
            ft.Container(
                content=ft.Text(cv_data.get('name', 'Unknown'), size=24, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                padding=ft.padding.all(20),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.center_left,
                    end=ft.alignment.center_right,
                    colors=["#4A90E2", "#9C27B0"]
                ),
                width=float('inf'),
                border_radius=10,
                margin=ft.margin.symmetric(horizontal=20)
            ),
            
            # Personal info
            ft.Container(
                content=personal_info,
                padding=ft.padding.symmetric(horizontal=20, vertical=10)
            ),
            
            # Skills and Education row
            ft.Container(
                content=ft.Row([
                    skills_section,
                    education_section
                ], spacing=15),
                padding=ft.padding.symmetric(horizontal=20, vertical=10)
            ),
            
            # Job History
            ft.Container(
                content=job_history_section,
                padding=ft.padding.symmetric(horizontal=20, vertical=10)
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
        ],
        spacing=0,
        padding=ft.padding.all(0),
        expand=True,
    )