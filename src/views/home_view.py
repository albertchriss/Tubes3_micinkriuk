import flet as ft
from components.search_configuration import SearchConfiguration
from components.results import Results
def home_view(page: ft.Page):

    def on_summary_click(cv_data):
        """Handle summary button click - navigate to CV summary view"""
        print(f"Summary clicked for: {cv_data.get('name', 'Unknown')}")
        # Store CV data in page data for access in routing
        page.client_storage.set("current_cv_data", cv_data)
        page.go("/summary")

    results = Results(on_summary_click=on_summary_click)

    def on_search_callback(search_data):
        """Handle search button click"""
        print(f"Search data: {search_data}")
        
        # Show results
        results.show_results()
        page.update()
        
        # Add your search logic here
    
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