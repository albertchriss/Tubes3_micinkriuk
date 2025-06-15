import flet as ft

class CVJobHistory:
    def __init__(self, cv_data):
        self.cv_data = cv_data
        self.container = self._create_job_history_container()
    
    def _create_job_history_container(self):
        # Job history items
        job_items = []
        job_history_list = self.cv_data.get('job_history', [])
        if job_history_list:
            for job in job_history_list:
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
        else:
            job_items.append(ft.Text("No job history data available", size=14, color="#666666"))
        
        return ft.Container(
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
                    content=ft.Column(job_items, spacing=10, scroll=ft.ScrollMode.AUTO),
                    padding=ft.padding.all(20),
                    bgcolor="#FFFFFF",
                    height=240,
                    alignment=ft.alignment.top_left,
                )
            ], spacing=0),
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color="#1A000000",
                offset=ft.Offset(0, 4)
            ),
        )