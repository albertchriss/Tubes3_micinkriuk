import flet as ft
from components.search_configuration import SearchConfiguration
from components.results import Results

def home_view(page: ft.Page):

    def on_summary_click(cv_data, cv_path):
        """Handle summary button click - navigate to CV summary view"""
        print(f"Summary clicked for: {cv_data.get('name', 'Unknown')}")
        # Store CV data in page data for access in routing
        page.client_storage.set("current_cv_data", cv_data)
        page.client_storage.set("current_cv_path", cv_path)
        page.go("/summary")

    results = Results(on_summary_click=on_summary_click)

    def on_search_callback(search_data):
        """I.S. search_data contains:
            keywords (list of string), 
            algorithm ("Knuth-Morris-Pratt", "Boyer-Moore", or "Aho-Corasick"), 
            and top_matches (int)"""

        print(f"Search data: {search_data}")
        
        # TODO: Add your search logic here
        # Your search function should return data in this format:
        # results_data = {
        #     "exact_match_stats": {"count": 15, "time_ms": 45},
        #     "fuzzy_match_stats": {"count": 8, "time_ms": 78},
        #     "applicants": [
        #         {
        #             "applicant_id": 1,
        #             "name": "John Doe",
        #             "matched_keywords": 3,
        #             "keywords_data": [{"keyword": "Python", "occurrences": 2}],
        #             "bgcolor": "#E3F2FD"
        #         }
        #     ]
        # }
        
        # Show results with sample data for now
        results.show_results()
        # results.show_results(results_data)  # Use this when you have real data
        page.update()
        
    search_config = SearchConfiguration(on_search_callback=on_search_callback)
    
    return ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "CV Analyzer App",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color="#4A90E2",
                        ),
                        ft.Text(
                            "Analyze and search through CVs efficiently",
                            size=16,
                            color="#424242",
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=20),
            ),
            # Search configuration
            search_config.container,

            # Results 
            results.container,

        ], spacing=20,
        scroll=ft.ScrollMode.AUTO),
        alignment=ft.alignment.top_center,
        padding=20,
        expand=True,
        bgcolor="#F5F5F5",
    )