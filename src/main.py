import flet as ft
from views.home_view import home_view
from views.cv_summary_view import cv_summary_view

def main(page: ft.Page):
    page.title = "CV Pattern Matching"
    page.padding = 0
    page.bgcolor = '#EAE6C9'
    page.window.full_screen = True
    page.fonts = {
        # "PGO": "/fonts/Pathway_Gothic_One/PathwayGothicOne-Regular.ttf",
        # "Freeman": "/fonts/Freeman/Freeman-Regular.ttf",
    }

    def route_change(route):
        page.views.clear()
        if page.route == "/" or page.route == "/views/home_view":
            page.views.append(
                ft.View(
                    route="/",
                    controls=[home_view(page)]
                )
            )   
        elif page.route.startswith("/summary"):
            # You'll need to pass CV data here
            cv_data = {}  # Get this from your state management
            page.views.append(
                ft.View(
                    route="/summary",
                    controls=[cv_summary_view(page, cv_data)]
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)
