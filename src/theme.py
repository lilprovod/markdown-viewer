from dataclasses import dataclass

@dataclass
class AppTheme:
     key:           str
     name:          str
     variant:       str
     
     BG_COLOR:           str
     ACCENT_COLOR:       str
     TEXTFIELD_COLOR:    str
     TEXTFIELD_BG_COLOR: str
     ERROR_BG_COLOR:     str

THEMES: dict[str, AppTheme] = {
     # ===== Purple ======
     "purple_dark": AppTheme(
          key="purple_dark",
          name="Purple",
          variant="dark",
          BG_COLOR="#211729",
          ACCENT_COLOR="#FF6FA8",
          TEXTFIELD_COLOR="#E8C3FF",
          TEXTFIELD_BG_COLOR="#402745",
          ERROR_BG_COLOR="#220A11",
     ),
     "purple_light": AppTheme(
          key="purple_light",
          name="Purple",
          variant="light",
          BG_COLOR="#FAF5FF",
          ACCENT_COLOR="#CC88DA",
          TEXTFIELD_COLOR="#392E4A",
          TEXTFIELD_BG_COLOR="#FFFFFF",
          ERROR_BG_COLOR="#F97373",
     ),
     
     # ===== Teal =====
     "teal_dark": AppTheme(
          key="teal_dark",
          name="Teal",
          variant="dark",
          BG_COLOR="#062827",
          ACCENT_COLOR="#2DD4BF",
          TEXTFIELD_COLOR="#E5F9F7",
          TEXTFIELD_BG_COLOR="#0B3533",
          ERROR_BG_COLOR="#F97373",
     ),
     "teal_light": AppTheme(
          key="teal_light",
          name="Teal",
          variant="light",
          BG_COLOR="#ECFEFF",
          ACCENT_COLOR="#0D9488",
          TEXTFIELD_COLOR="#022C22",
          TEXTFIELD_BG_COLOR="#FFFFFF",
          ERROR_BG_COLOR="#F97373",
     ),
     
     # ===== Orange =====
     "orange_dark": AppTheme(
          key="orange_dark",
          name="Orange",
          variant="dark",
          BG_COLOR="#1F1308",
          ACCENT_COLOR="#FB923C",
          TEXTFIELD_COLOR="#FFF7ED",
          TEXTFIELD_BG_COLOR="#271509",
          ERROR_BG_COLOR="#F97373",
     ),
     "orange_light": AppTheme(
          key="orange_light",
          name="Orange",
          variant="light",
          BG_COLOR="#FFF7ED",
          ACCENT_COLOR="#F97316",
          TEXTFIELD_COLOR="#1F2933",
          TEXTFIELD_BG_COLOR="#FFFFFF",
          ERROR_BG_COLOR="#F97373",
     ),
}

DEFAULT_THEME_KEY = "purple_dark"


def get_theme(theme_key: str) -> AppTheme:
     return THEMES.get(theme_key, THEMES[DEFAULT_THEME_KEY])


def available_theme_bases() -> list[str]:
     """ Список базовых тем: purple / teal / orange ... """
     bases = set(k.split("_")[0] for k in THEMES.keys())
     return sorted(bases)


test_input = """
# **Это пример работы _данного_ приложения.**
-- --
Функционал:
1. Может в прямом эфире переводить текст в markdown-формат;
2. Может считать количество введённых символов и моментально выводить его;
3. Содержит следующие темы:
     * *PURPLE*
4. Добавлено сохранения *последнего введённого текста* до закрытия приложения.
-- --
"""