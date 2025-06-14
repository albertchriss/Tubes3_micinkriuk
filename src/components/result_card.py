import flet as ft

class ResultCard:
    def __init__(self, name, matched_keywords, keywords_data, bgcolor="#E3F2FD"):
        self.name = name
        self.matched_keywords = matched_keywords
        self.keywords_data = keywords_data  # List of {keyword: string, occurrences: int}
        self.bgcolor = bgcolor
        
        self.container = self._create_card()
    
    def _create_card(self):
        """Create the CV card container"""
        
        # Create keyword occurrence widgets in rows (keyword and occurrence on same line)
        keyword_widgets = []
        for i, keyword_data in enumerate(self.keywords_data, 1):
            keyword_widgets.append(
                ft.Row([
                    ft.Text(f"{i}. {keyword_data['keyword']}", size=14, color="#666666", expand=True),
                    ft.Container(
                        content=ft.Text(f"{keyword_data['occurrences']} occurrence{'s' if keyword_data['occurrences'] != 1 else ''}", 
                                       size=12, color="#FFFFFF"),
                        bgcolor="#4A90E2",
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=15
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )
        
        # Create scrollable keywords section with fixed height for 3 keywords
        # Each keyword row is approximately 35px, so 3 rows = 105px
        keywords_section = ft.Container(
            content=ft.Column(
                controls=keyword_widgets,
                spacing=5,
                scroll=ft.ScrollMode.HIDDEN if len(keyword_widgets) > 3 else None
            ),
            height=105,  # Fixed height for 3 keywords
            padding=ft.padding.symmetric(vertical=5),
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text(self.name, size=20, weight=ft.FontWeight.BOLD, color="#424242"),
                ft.Text(f"{self.matched_keywords} matched keyword{'s' if self.matched_keywords != 1 else ''}", 
                        size=14, color="#666666"),
                
                # Add some spacing before keywords
                ft.Container(height=10),
                
                # Fixed height keywords section
                keywords_section,
                
                # Add spacing before buttons
                ft.Container(height=15),
                
                # Action buttons
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
                        expand=True
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
                        expand=True
                    ),
                ], spacing=15)
            ], spacing=5),
            padding=ft.padding.all(20),
            bgcolor=self.bgcolor,
            border_radius=12,
            border=ft.border.all(1, "#D0D0D0"),
            expand=True
        )