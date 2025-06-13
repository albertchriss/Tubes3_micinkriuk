import flet as ft

def home_view(page: ft.Page):

    algorithms = ft.SegmentedButton(
        segments=[
            ft.Segment(value="Knuth-Morris-Pratt", label=ft.Text("Knuth-Morris-Pratt", size=14)),
            ft.Segment(value="Boyer-Moore", label=ft.Text("Boyer-Moore", size=14)),
            ft.Segment(value="Aho-Corasick", label=ft.Text("Aho-Corasick", size=14)),
        ],
        selected={"Knuth-Morris-Pratt"},  # default value
        show_selected_icon=False,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=4),
            padding=ft.padding.symmetric(horizontal=14, vertical=12),
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

    top_matches = ft.TextField(
        hint_text="0",
        color="#424242",
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.NumbersOnlyInputFilter(),
    )

    keywords_field = ft.TextField(
        hint_text="React, Express, HTML",
        color="#424242",
    )
    
    search_button = ft.ElevatedButton(
        "Search", 
        icon=ft.Icons.SEARCH,
        color="#FFFFFF",
        on_click=lambda e: print("Search clicked"),
        bgcolor="#4A90E2",   
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(horizontal=50, vertical=15),
            text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD),
        ) 
    )
    
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
            
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text("Search Configuration"
                                        , size=20, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
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
                                ft.Text(
                                    "Keywords:",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color="#424242"
                                ),
                                keywords_field,
                            ], expand=True, spacing=15),
                            
                            ft.Column([
                                ft.Text(
                                    "Search Algorithm:",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color="#424242"
                                ),
                                algorithms,
                            ], expand=True, spacing=15),
                            
                            ft.Column([
                                ft.Text(
                                    "Top Matches:",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color="#424242"
                                ),
                                top_matches,
                            ], expand=True, spacing=15),
                        ], 
                        spacing=20, 
                        ),
                        padding=ft.padding.symmetric(horizontal=20, vertical=20),
                    ),
                    
                    ft.Container(
                        content=search_button,
                        alignment=ft.alignment.center,
                        padding=ft.padding.all(20),
                    ),
                ]),
                border_radius=10,
                bgcolor="white",
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.1, "#000000"),
                    offset=ft.Offset(0, 4)
                ),
            ),
        ]),
        alignment=ft.alignment.center,
        padding=20,
        expand=True,
        bgcolor="#F5F5F5",
    )