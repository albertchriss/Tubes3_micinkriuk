import flet as ft
from .result_card import ResultCard

class Results:
    def __init__(self, on_summary_click=None):
        self.on_summary_click = on_summary_click
        self.container = self._create_results_container()
        
        # Sample data - now without cv_data
        self.sample_data = {
            "exact_match_stats": {
                "count": 15,
                "time_ms": 45
            },
            "fuzzy_match_stats": {
                "count": 8,
                "time_ms": 78
            },
            "applicants": [
                {
                    "applicant_id": 1,
                    "name": "Farhan Abdullah",
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
                    "applicant_id": 2,
                    "name": "Sarah Johnson",
                    "matched_keywords": 3,
                    "keywords_data": [
                        {"keyword": "Python", "occurrences": 2},
                        {"keyword": "Django", "occurrences": 1},
                        {"keyword": "SQL", "occurrences": 3}
                    ],
                    "bgcolor": "#F3E5F5"
                },
                {
                    "applicant_id": 3,
                    "name": "Michael Smith",
                    "matched_keywords": 5,
                    "keywords_data": [
                        {"keyword": "JavaScript", "occurrences": 4},
                        {"keyword": "Node.js", "occurrences": 2},
                        {"keyword": "MongoDB", "occurrences": 1}
                    ],
                    "bgcolor": "#E8F5E9"
                },
                {
                    "applicant_id": 4,
                    "name": "Emily Davis",
                    "matched_keywords": 2,
                    "keywords_data": [
                        {"keyword": "Java", "occurrences": 1},
                        {"keyword": "Spring", "occurrences": 2}
                    ],
                    "bgcolor": "#FFF3E0"
                },
                {
                    "applicant_id": 5,
                    "name": "David Wilson",
                    "matched_keywords": 6,
                    "keywords_data": [
                        {"keyword": "C#", "occurrences": 3},
                        {"keyword": ".NET", "occurrences": 2},
                        {"keyword": "Azure", "occurrences": 1}
                    ],
                    "bgcolor": "#E3F2FD"
                },
                {
                    "applicant_id": 6,
                    "name": "Olivia Brown",
                    "matched_keywords": 4,
                    "keywords_data": [
                        {"keyword": "PHP", "occurrences": 2},
                        {"keyword": "Laravel", "occurrences": 1},
                        {"keyword": "MySQL", "occurrences": 3}
                    ],
                    "bgcolor": "#F3E5F5"
                }
            ]
        }

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
                            border=ft.border.only(left=ft.BorderSide(4, "#4A90E2")),
                            width=float('inf'),
                        ),
                    ]),
                    padding=ft.padding.all(20),
                ),
                
                # CV Cards section - this will be populated dynamically
                ft.Container(
                    content=ft.Column([], spacing=15),  # Empty initially
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
        """
        Show results with given data or sample data
        Expected results_data format:
        {
            "exact_match_stats": {"count": int, "time_ms": int},
            "fuzzy_match_stats": {"count": int, "time_ms": int},
            "applicants": [
                {
                    "applicant_id": int,
                    "name": str,
                    "matched_keywords": int,
                    "keywords_data": [{"keyword": str, "occurrences": int}],
                    "bgcolor": str (optional)
                }
            ]
        }
        """
        if results_data is None:
            results_data = self.sample_data
        
        # Update stats
        exact_stats = results_data.get("exact_match_stats", {})
        fuzzy_stats = results_data.get("fuzzy_match_stats", {})
        
        exact_text = f"Exact Match: {exact_stats.get('count', 0)} CVs scanned in {exact_stats.get('time_ms', 0)}ms."
        fuzzy_text = f"Fuzzy Match: {fuzzy_stats.get('count', 0)} CVs scanned in {fuzzy_stats.get('time_ms', 0)}ms."
        
        self.update_stats(exact_text, fuzzy_text)

        # Create result cards and organize them into rows (max 5 per row)
        card_rows = []
        applicants = results_data.get("applicants", [])

        # If no applicants, show a message
        if(len(applicants) == 0):
            no_results_container = ft.Container(
                content=ft.Column([
                    # Empty state icon
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.SEARCH_OFF,
                            size=80,
                            color="#B0BEC5"
                        ),
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(bottom=20)
                    ),
                    
                    # Main message
                    ft.Text(
                        "No Applicants Found",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#424242",
                        text_align=ft.TextAlign.CENTER
                    ),
                    
                    # Subtitle message
                    ft.Text(
                        "We couldn't find any applicants matching your search criteria.",
                        size=16,
                        color="#757575",
                        text_align=ft.TextAlign.CENTER
                    ),
                    
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(40),
                alignment=ft.alignment.center,
                bgcolor="#FFFFFF",
                border_radius=12,
                border=ft.border.all(2, "#E3F2FD"),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color="#1A000000",
                    offset=ft.Offset(0, 2)
                ),
                margin=ft.margin.symmetric(horizontal=40, vertical=20)
            )
            
            # Center the no results container
            card_rows.append(
                ft.Row(
                    controls=[no_results_container],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )
            
            # Update the CV Cards section
            cards_column = self.container.content.controls[2].content
            cards_column.controls = card_rows
            self.container.visible = True
            return
        
        # Group applicants into chunks of 4
        for i in range(0, len(applicants), 4):
            applicant_chunk = applicants[i:i+4]
            
            # Create cards for this chunk
            row_cards = []
            for applicant in applicant_chunk:
                card = ResultCard(
                    applicant_id=applicant["applicant_id"],
                    name=applicant["name"],
                    matched_keywords=applicant["matched_keywords"],
                    keywords_data=applicant["keywords_data"],
                    bgcolor=applicant.get("bgcolor", "#E3F2FD"),
                    on_summary_click=self.on_summary_click
                )
                card.container.expand = True
                row_cards.append(card.container)
            
            # Create a row with up to 5 cards - align to start to prevent stretching
            card_row = ft.Row(
                controls=row_cards,
                spacing=15,
                alignment=ft.MainAxisAlignment.START,  # Align cards to the left
            )
            card_rows.append(card_row)
        
        # Update the CV Cards section with multiple rows
        cards_column = self.container.content.controls[2].content
        cards_column.controls = card_rows
        
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