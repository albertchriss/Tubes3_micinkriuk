import flet as ft
import views.home_view as halo

def main(page: ft.Page):
    page.title = "CV Pattern Matching"
    page.padding = 0
    page.bgcolor = '#EAE6C9'
    page.window.height = 800
    page.window.width = 1300

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
                    controls=[halo.home_view(page)]
                )
            )   
        elif page.route == "/views/searchPage":
            page.views.append(
                ft.View(
                    route="/views/searchPage",
                    # controls=[create_search_page(page)]
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
