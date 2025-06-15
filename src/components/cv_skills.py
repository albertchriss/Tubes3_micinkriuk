import flet as ft

class CVSkills:
    def __init__(self, cv_data):
        self.cv_data = cv_data
        self.container = self._create_skills_container()
    
    def _create_skills_container(self):
        skills_chips = []
        skills_list = self.cv_data.get('skills', [])
        if skills_list:
            for skill in skills_list:
                skills_chips.append(
                    ft.Container(
                        content=ft.Text(skill, size=14, color="#FFFFFF"),
                        bgcolor="#4A90E2",
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=15,
                        margin=ft.margin.only(right=8, bottom=8)
                    )
                )
        else:
            skills_chips.append(ft.Text("No skills data available", size=14, color="#666666"))
        
        return ft.Container(
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
                        ft.Row(skills_chips, wrap=True)
                    ]),
                    padding=ft.padding.all(20),
                    bgcolor="#FFFFFF",
                    height=150, 
                    alignment=ft.alignment.top_left
                )
            ], spacing=0),
            border_radius=10,
            expand=True,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color="#1A000000",
                offset=ft.Offset(0, 4)
            ),
        )