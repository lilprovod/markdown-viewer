import flet as ft
from theme import get_theme, DEFAULT_THEME_KEY, available_theme_bases


def build_app_bar(page: ft.Page,
                  open_md_file, save_md_file, open_settings,) -> None:
    theme_key = page.client_storage.get("theme_key") or DEFAULT_THEME_KEY
    t = get_theme(theme_key)
    
    # ====== AppBar ======
    
    page.appbar = ft.AppBar(
        title=ft.Text("Markdown Viewer", weight=ft.FontWeight.BOLD),
        center_title=False,
        bgcolor=t.BG_COLOR,
        color=t.TEXTFIELD_COLOR,
        actions=[
            ft.IconButton(
                ft.icons.FILE_OPEN,
                tooltip="Open Markdown file",
                on_click=open_md_file
            ),
            ft.IconButton(
                ft.icons.SAVE,
                tooltip="Save Markdown file",
                on_click=save_md_file
            ),
            ft.IconButton(
                ft.icons.SETTINGS,
                tooltip="Open app settings",
                on_click=open_settings
            ),
        ]
    )

def build_main_window(page: ft.Page) -> None:
    # ====== Настройка темы ======
    
    theme_key = page.client_storage.get("theme_key") or DEFAULT_THEME_KEY
    t = get_theme(theme_key)
    
    page.bgcolor = t.BG_COLOR
    page.theme_mode = (
        ft.ThemeMode.DARK if t.variant == "dark" else ft.ThemeMode.LIGHT
    )
    
    # ====== Восстанавливаем последний введённый текст ======
    last_input = page.client_storage.get("last_input_text") or ""
    
    
    # ====== Markdown-виджет ======
    output_field = ft.Markdown(
        last_input,
        selectable=True,
    )
    
    
    # ====== Обновление Markdown и сохранение в client_storage ======
    def update_markdown_widget(e):
        output_field.value = e.control.value
        
        page.client_storage.set("last_input_text", e.control.value)
        
        output_field.update()
    
    
    # ====== Поле ввода ======
    input_field = ft.TextField(
        last_input,
        label="Input your markdown text here...",
        label_style=ft.TextStyle(color=t.TEXTFIELD_COLOR,
                                 weight=ft.FontWeight.BOLD),
        multiline=True,
        min_lines=30,
        max_lines=30,
        counter_text="{value_length} chars",
        icon=ft.Icon(ft.icons.TEXT_FIELDS, color=t.ACCENT_COLOR),
        on_change=update_markdown_widget, #! markdown update
        filled=True,
        color=t.TEXTFIELD_COLOR,
        counter_style=ft.TextStyle(color=t.ACCENT_COLOR,
                                   weight=ft.FontWeight.BOLD),
        cursor_color=t.ACCENT_COLOR,
        bgcolor=t.TEXTFIELD_BG_COLOR,
        border_color=t.ACCENT_COLOR,
        border=ft.InputBorder.NONE,
        expand=True,
    )
    
    
    def on_file_picked(e: ft.FilePickerResultEvent):
        if not e.files:
            return
        
        file = e.files[0]
        try:
            with open(file.path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Error reading file: {ex}"),
                bgcolor=t.ERROR_BG_COLOR,
            )
            
            page.snack_bar.open = True
            page.update()
            return
        
        input_field.value = text
        output_field.value = text
        
        page.client_storage.set("last_input_text", text)
        
        input_field.update()
        output_field.update()
    
    file_picker = ft.FilePicker(
        on_result=on_file_picked,
    )
    page.overlay.append(file_picker)
    
    
    def open_md_file(e):
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["md", "markdown", "txt"]
        )
    
    def on_file_saved(e):
        if not e.path:
            return
        
        try:
            with open(e.path, "w", encoding="utf-8") as f:
                f.write(input_field.value or "")
        except Exception as ex:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Error saving file: {ex}"),
                bgcolor=t.ERROR_BG_COLOR,
            )
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"File successfully saved to {e.path}"),
            )
        
        page.snack_bar.open = True
        page.update()
    
    
    file_saver = ft.FilePicker(
        on_result=on_file_saved,
    )
    page.overlay.append(file_saver)
    
    def save_md_file(e):
        file_saver.save_file(
            file_name="output.md",
            allowed_extensions=["md", "markdown", "txt"]
        )
    
    # ==== Окно настроек =====
    def current_theme_key():
        return page.client_storage.get("theme_key") or DEFAULT_THEME_KEY

    
    def apply_theme(base: str | None = None, variant: str | None = None):
        actual_key  = current_theme_key()
        base        = base or actual_key.split("_")[0]
        variant     = variant or get_theme(actual_key).variant
        
        page.client_storage.set("theme_key", f"{base}_{variant}")
        
        page.dialog = None
        page.controls.clear()
        build_main_window(page)
    
    
    def open_settings(e):
        actual_key      = current_theme_key()
        actual_theme    = get_theme(actual_key)
        actual_base     = actual_key.split("_")[0]
        actual_variant  = actual_theme.variant
        
        dark_switch = ft.Switch(
            label="Dark Mode",
            value=(actual_variant == "dark")
        )
        
        def on_dark_mode_switch(e):
            actual_base = current_theme_key().split("_")[0]
            new_variant = "dark" if e.control.value else "light"
            
            apply_theme(base=actual_base, variant=new_variant)
            
            close_settings(e)
    
        dark_switch.on_change = on_dark_mode_switch
        
        def swatch(base_key: str):
            accent = get_theme(f"{base_key}_{actual_variant}").ACCENT_COLOR
            is_current = (base_key == actual_base)
            border = ft.border.all(
                3 if is_current else 0,
                t.TEXTFIELD_COLOR if is_current else accent,
            )
            
            def on_theme_click(e):
                apply_theme(
                    base=base_key, variant="dark" if dark_switch.value else "light"
                )
                close_settings(e)
            
            return ft.Container(
                height=48,
                width=240,
                bgcolor=accent,
                border_radius=20,
                border=border,
                tooltip=base_key.capitalize(),
                ink=True,
                on_click=on_theme_click
            )
    
        theme_buttons_col = ft.Column(
            [
                swatch("purple"),
                swatch( "teal" ),
                swatch("orange"),
            ],
            spacing=8,
            width=240,
        )
        
        def close_settings(e):
            settings_dialog.open = False
            page.update()
    
        settings_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Settings"),
            content=ft.Column(
                [
                    dark_switch,
                    theme_buttons_col,
                    ft.Row(),
                    ft.Row(),
                    ft.Row(
                        [
                            ft.Text("maked by lilprovod with <3",
                                    color=t.TEXTFIELD_COLOR,
                                    size=12,
                            )
                        ],
                        ft.MainAxisAlignment.CENTER
                    ),
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton("Close", on_click=close_settings),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.dialog = settings_dialog
        settings_dialog.open = True
        page.update()
    
    build_app_bar(page, open_md_file, save_md_file, open_settings)
    
    
    left_panel = ft.Container(
        content=ft.Column(
            [input_field],
            expand=True
        ),
        expand=1,
        padding=10
    )
    
    right_panel = ft.Container(
        content=ft.Column(
            [output_field],
            expand=True,
            scroll=ft.ScrollMode.AUTO
        ),
        expand=1,
        padding=10
    )
    
    row = ft.Row(
        [
            left_panel,
            ft.VerticalDivider(width=1, color=t.ACCENT_COLOR),
            right_panel,
        ],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH
    )
    
    page.add(
        ft.Container(
            content=row,
            expand=True,
        )
    )
    page.update()
