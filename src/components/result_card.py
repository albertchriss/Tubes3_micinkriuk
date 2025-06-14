import flet as ft

class ResultCard:
    def __init__(self, name, matched_keywords, keywords_data, bgcolor="#E3F2FD", on_summary_click=None, cv_data=None):
        self.name = name
        self.matched_keywords = matched_keywords
        self.keywords_data = keywords_data
        self.bgcolor = bgcolor
        self.on_summary_click = on_summary_click
        self.cv_data = cv_data or {}
        
        self.container = self._create_card()
    
    def _on_summary_clicked(self, e):
        print(f"Summary clicked! CV Data: {self.cv_data}")  # Add this debug line
        if self.on_summary_click:
            self.on_summary_click(self.cv_data)
    
    def _create_card(self):
        """Create the CV card container"""
        
        # Create keyword occurrence widgets in rows
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
                        expand=True,
                        on_click=self._on_summary_clicked  # Add click handler
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