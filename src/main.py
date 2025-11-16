import flet as ft
from gui import build_main_window


def main(page: ft.Page):
    page.title = "Markdown Viewer"
    page.window.height = 800
    page.window.width = 1200
    
    page.theme_mode = ft.ThemeMode.DARK
    
    build_main_window(page)
    
    page.update()


if __name__ == "__main__":
    ft.app(target=main)