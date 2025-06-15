import flet as ft

class CVPersonalInfo:
    def __init__(self, cv_data):
        self.cv_data = cv_data
        self.container = self._create_personal_info_container()
    
    def _create_personal_info_container(self):
        return ft.Container(
            content=ft.Column([
                ft.Text(self.cv_data.get('name', 'Unknown'), size=24, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                ft.Container(height=10),  

                ft.Row([
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CALENDAR_MONTH, color="#4A90E2", size=16),
                            ft.Text(f"Birthdate: {self.cv_data.get('birthdate', 'DD-MM-YYYY')}", size=14, color="#424242")
                        ], spacing=8),
                        bgcolor="#E3F2FD",
                        padding=ft.padding.all(10),
                        border_radius=8,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.LOCATION_ON, color="#9C27B0", size=16),
                            ft.Text(f"Address: {self.cv_data.get('address', 'N/A')}", size=14, color="#424242")
                        ], spacing=8),
                        bgcolor="#F3E5F5",
                        padding=ft.padding.all(10),
                        border_radius=8,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.PHONE, color="#4A90E2", size=16),
                            ft.Text(f"Phone: {self.cv_data.get('phone', 'N/A')}", size=14, color="#424242")
                        ], spacing=8),
                        bgcolor="#E3F2FD",
                        padding=ft.padding.all(10),
                        border_radius=8,
                        expand=True
                    ),
                ], spacing=10)
            ], horizontal_alignment=ft.CrossAxisAlignment.START),
            padding=ft.padding.all(20),
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=["#4A90E2", "#9C27B0"]
            ),
            border_radius=10,
            margin=ft.margin.symmetric(horizontal=20, vertical=10),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color="#1A000000",
                offset=ft.Offset(0, 4)
            ),
        )