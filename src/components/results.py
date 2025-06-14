import flet as ft
from .result_card import ResultCard

class Results:
    def __init__(self):
        self.container = self._create_results_container()
        
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
                "bgcolor": "#E3F2FD"
            },
            {
                "name": "Alana", 
                "matched_keywords": 1,
                "keywords_data": [
                    {"keyword": "React", "occurrences": 3}
                ],
                "bgcolor": "#F3E5F5"
            },
            {
                "name": "Ariel",
                "matched_keywords": 1, 
                "keywords_data": [
                    {"keyword": "HTML", "occurrences": 4}
                ],
                "bgcolor": "#E8F5E8"
            }
        ]
    
    def _create_results_container(self):
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
                            border=ft.border.only(left=ft.BorderSide(4, "#4A90E2")),
                            width=float('inf'),
                        ),
                    ]),
                    padding=ft.padding.only(left=20, right=20, top=10, bottom=10),
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
                bgcolor=result["bgcolor"]
            )
            result_cards.append(card.container)
        
        # Update the CV Cards section with new cards
        cards_row = self.container.content.controls[2].content  # Get the Row container
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