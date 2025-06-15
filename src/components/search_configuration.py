import flet as ft

class SearchConfiguration:
    def __init__(self, on_search_callback=None):
        self.on_search_callback = on_search_callback
        
        # Create components
        self.algorithms = ft.SegmentedButton(
            segments=[
                ft.Segment(value="Knuth-Morris-Pratt", label=ft.Text("Knuth-Morris-Pratt", size=14)),
                ft.Segment(value="Boyer-Moore", label=ft.Text("Boyer-Moore", size=14)),
                ft.Segment(value="Aho-Corasick", label=ft.Text("Aho-Corasick", size=14)),
            ],
            selected={"Knuth-Morris-Pratt"},
            show_selected_icon=False,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=4),
                padding=ft.padding.symmetric(horizontal=14, vertical=22),
                bgcolor={
                    ft.ControlState.SELECTED: "#4A90E2",  
                    ft.ControlState.DEFAULT: "#FFFFFF"    
                },
                color={
                    ft.ControlState.SELECTED: "#FFFFFF",  
                    ft.ControlState.DEFAULT: "#424242"    
                },
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(1, "#000000"),
                    ft.ControlState.SELECTED: ft.BorderSide(1, "#4A90E2")
                }
            )
        )

        self.top_matches = ft.TextField(
            hint_text="0",
            color="#424242",
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.NumbersOnlyInputFilter(),
        )

        self.keywords_field = ft.TextField(
            hint_text="React, Express, HTML",
            color="#424242",
        )

        self.search_button = ft.ElevatedButton(
            "Search", 
            icon=ft.Icons.SEARCH,
            color="#FFFFFF",
            on_click=self._on_search_clicked,
            bgcolor="#4A90E2",   
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.padding.symmetric(horizontal=50, vertical=15),
                text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD),
            ) 
        )

        # Create the main container
        self.container = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text("Search Configuration", size=20, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    padding=ft.padding.all(20),
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=["#4A90E2", "#50E3C2"],
                    ),
                    width=float('inf'),
                ),
                
                ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text("Keywords:", size=14, weight=ft.FontWeight.BOLD, color="#424242"),
                            self.keywords_field,
                        ], expand=True, spacing=15),
                        
                        ft.Column([
                            ft.Text("Search Algorithm:", size=14, weight=ft.FontWeight.BOLD, color="#424242"),
                            self.algorithms,
                        ], expand=True, spacing=15),
                        
                        ft.Column([
                            ft.Text("Top Matches:", size=14, weight=ft.FontWeight.BOLD, color="#424242"),
                            self.top_matches,
                        ], expand=True, spacing=15),
                    ], spacing=20),
                    padding=ft.padding.symmetric(horizontal=20, vertical=20),
                ),
                
                ft.Container(
                    content=self.search_button,
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(20),
                ),
            ]),
            border_radius=10,
            bgcolor="white",
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color="#1A000000",  # Fixed the shadow color
                offset=ft.Offset(0, 4)
            ),
        )
    
    def _on_search_clicked(self, e):
        if self.on_search_callback:
            if(self.keywords_field.value == "" or self.top_matches.value == ""):
                return
            
            if(self.top_matches.value.isdigit() == False or int(self.top_matches.value) <= 0):
                return
            
            # Get values and pass to callback
            search_data = {
                'keywords': list(dict.fromkeys(keyword.strip() for keyword in self.keywords_field.value.split(',') if keyword.strip())),
                'algorithm': list(self.algorithms.selected)[0] if self.algorithms.selected else None,
                'top_matches': self.top_matches.value
            }
            self.on_search_callback(search_data)
    
    # def get_values(self):
    #     """Get current form values"""
    #     return {
    #         'keywords': self.keywords_field.value,
    #         'algorithm': list(self.algorithms.selected)[0] if self.algorithms.selected else None,
    #         'top_matches': self.top_matches.value
    #     }