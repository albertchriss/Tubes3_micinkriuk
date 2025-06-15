import flet as ft
from components.search_configuration import SearchConfiguration
from components.results import Results
from core.service import search_matching_data

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

        # print(f"Search data: {search_data}")
        results_data = search_matching_data(
            keywords=search_data["keywords"],
            algo=search_data["algorithm"],
            top_match=int(search_data["top_matches"])
        )
        try:
            page.client_storage.set("cached_results_data", results_data)
            print("Results cached successfully")
        except Exception as e:
            print(f"Error caching results: {e}")
        
        # Show results with sample data for now
        # results.show_results()
        results.show_results(results_data)  # Use this when you have real data
        page.update()
        
    def restore_cached_results():
        """Restore cached results if they exist"""
        try:
            cached_data = page.client_storage.get("cached_results_data")
            if cached_data is not None:
                print("Restoring cached results...")
                results.show_results(cached_data)
                page.update()
                return True
            else:
                print("No cached results found")
                return False
        except Exception as e:
            print(f"Error restoring cached results: {e}")
            return False
        
    # Try to restore cached results when the view loads
    restore_cached_results()
    
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