import flet as ft
from .result_card import ResultCard

class Results:
    def __init__(self, on_summary_click=None):
        self.on_summary_click = on_summary_click
        self.container = self._create_results_container()
        
        # Sample data with CV details
        self.sample_data = [
            {
                "name": "Farhan",
                "matched_keywords": 4,
                "keywords_data": [
                    {"keyword": "React", "occurrences": 1},
                    {"keyword": "Express", "occurrences": 2},
                    {"keyword": "HTML", "occurrences": 3},
                    {"keyword": "CSS", "occurrences": 1}
                ],
                "bgcolor": "#E3F2FD",
                "cv_data": {
                    "name": "Farhan",
                    "birthdate": "15-03-1995",
                    "address": "Jalan Sariasih Sarijadi ITB",
                    "phone": "0812-3456-7890",
                    "skills": ["JavaScript", "React", "Node.js", "Express", "HTML", "CSS", "MongoDB"],
                    "education": [
                        {
                            "degree": "Informatics Engineering",
                            "institution": "Institut Teknologi Bandung",
                            "year": "2022-2026"
                        }
                    ],
                    "job_history": [
                        {
                            "position": "CTO",
                            "description": "Leading the organization's technology strategies",
                            "year": "2000-2004"
                        },
                        {
                            "position": "Senior Developer",
                            "description": "Developing and maintaining web applications",
                            "year": "1998-2000"
                        }
                    ]
                }
            },
            # Add more sample data as needed...
        ]

    def _create_results_container(self):
        """Create the main results container"""
        return ft.Container(
            content=ft.Column([
                # Results header
                ft.Container(
                    content=ft.Text("Results", size=20, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    padding=ft.padding.all(20),
                    bgcolor="#6C63FF",
                    width=float('inf'),
                ),
                
                # Stats section
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Exact Match: 15 CVs scanned in 45ms.", color="#4A90E2", size=14),
                                ft.Text("Fuzzy Match: 8 CVs scanned in 78ms.", color="#9C27B0", size=14),
                            ]),
                            padding=ft.padding.all(15),
                            bgcolor="#E3F2FD",
                            border_radius=8,
                            border=ft.border.only(left=ft.BorderSide(4, "#4A90E2"))
                        ),
                    ]),
                    padding=ft.padding.all(20),
                ),
                
                # CV Cards section - this will be populated dynamically
                ft.Container(
                    content=ft.Row([], spacing=15),  # Empty initially
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                ),
            ]),
            border_radius=10,
            bgcolor="white",
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color="#1A000000",
                offset=ft.Offset(0, 4)
            ),
            visible=False  # Initially hidden
        )
    
    def show_results(self, results_data=None):
        """Show results with given data or sample data"""
        if results_data is None:
            results_data = self.sample_data
            
        # Create result cards
        result_cards = []
        for result in results_data:
            card = ResultCard(
                name=result["name"],
                matched_keywords=result["matched_keywords"],
                keywords_data=result["keywords_data"],
                bgcolor=result["bgcolor"],
                on_summary_click=self.on_summary_click,
                cv_data=result.get("cv_data", {})
            )
            result_cards.append(card.container)
        
        # Update the CV Cards section with new cards
        cards_row = self.container.content.controls[2].content
        cards_row.controls = result_cards
        
        # Show the results container
        self.container.visible = True
    
    def hide_results(self):
        """Hide the results container"""
        self.container.visible = False
    
    def update_stats(self, exact_match_info="", fuzzy_match_info=""):
        """Update the stats section"""
        stats_container = self.container.content.controls[1].content.controls[0].content
        if exact_match_info:
            stats_container.controls[0].value = exact_match_info
        if fuzzy_match_info:
            stats_container.controls[1].value = fuzzy_match_info