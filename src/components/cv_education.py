import flet as ft

class CVEducation:
    def __init__(self, cv_data):
        self.cv_data = cv_data
        self.container = self._create_education_container()
    
    def _create_education_container(self):
        # Education items
        education_items = []
        education_list = self.cv_data.get('education', [])
        if education_list:
            for edu in education_list:
                education_items.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(edu.get('degree', 'N/A'), size=16, weight=ft.FontWeight.BOLD, color="#4A90E2"),
                            ft.Text(edu.get('institution', 'N/A'), size=14, color="#666666"),
                            ft.Text(edu.get('year', 'N/A'), size=12, color="#999999")
                        ], spacing=2, width=float('inf')),
                        padding=ft.padding.all(15),
                        bgcolor="#F8F9FA",
                        border_radius=8,
                        border=ft.border.only(left=ft.BorderSide(4, "#4A90E2"))
                    )
                )
        else:
            education_items.append(ft.Text("No education data available", size=14, color="#666666"))
        
        return ft.Container(
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
                    content=ft.Column(education_items, spacing=10, scroll=ft.ScrollMode.AUTO),
                    padding=ft.padding.all(20),
                    bgcolor="#FFFFFF",
                    height=150,  # Fixed height to match skills
                    alignment=ft.alignment.top_left,
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