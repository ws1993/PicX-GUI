"""Theme configuration for PicX GUI - Flet version."""
import flet as ft
from typing import Dict, Any


# 主题颜色配置
COLORS = {
    # 主色调 - 琥珀色系
    "primary": ft.Colors.AMBER,
    "primary_hover": ft.Colors.AMBER_700,
    "primary_light": ft.Colors.AMBER_100,
    "primary_disabled": ft.Colors.AMBER_200,
    
    # 背景和表面颜色
    "background": ft.Colors.GREY_50,
    "surface": ft.Colors.WHITE,
    "surface_light": ft.Colors.GREY_50,
    "surface_dark": ft.Colors.GREY_100,
    "border": ft.Colors.GREY_300,
    "border_light": ft.Colors.GREY_200,
    
    # 文本颜色
    "text": ft.Colors.GREY_900,
    "text_secondary": ft.Colors.GREY_700,
    "text_muted": ft.Colors.GREY_500,
    
    # 状态颜色
    "success": ft.Colors.GREEN,
    "success_light": ft.Colors.GREEN_100,
    "warning": ft.Colors.ORANGE,
    "warning_light": ft.Colors.ORANGE_100,
    "error": ft.Colors.RED,
    "error_light": ft.Colors.RED_100,
    "info": ft.Colors.BLUE,
    "info_light": ft.Colors.BLUE_100,
}

# 深色主题颜色
DARK_COLORS = {
    # 主色调 - 琥珀色系
    "primary": ft.Colors.AMBER,
    "primary_hover": ft.Colors.AMBER_300,
    "primary_light": ft.Colors.AMBER_900,
    "primary_disabled": ft.Colors.AMBER_800,
    
    # 背景和表面颜色
    "background": ft.Colors.GREY_900,
    "surface": ft.Colors.GREY_800,
    "surface_light": ft.Colors.GREY_700,
    "surface_dark": ft.Colors.GREY_900,
    "border": ft.Colors.GREY_700,
    "border_light": ft.Colors.GREY_800,
    
    # 文本颜色
    "text": ft.Colors.WHITE,
    "text_secondary": ft.Colors.GREY_300,
    "text_muted": ft.Colors.GREY_500,
    
    # 状态颜色
    "success": ft.Colors.GREEN_300,
    "success_light": ft.Colors.GREEN_900,
    "warning": ft.Colors.ORANGE_300,
    "warning_light": ft.Colors.ORANGE_900,
    "error": ft.Colors.RED_300,
    "error_light": ft.Colors.RED_900,
    "info": ft.Colors.BLUE_300,
    "info_light": ft.Colors.BLUE_900,
}

# 字体配置
FONTS = {
    "heading": 24,
    "subheading": 18,
    "title": 16,
    "body": 14,
    "body_bold": 14,
    "small": 12,
    "caption": 10,
}

# 尺寸配置
SIZES = {
    "window_width": 1200,
    "window_height": 800,
    "min_width": 800,
    "min_height": 600,
    "padding": 20,
    "padding_small": 10,
    "corner_radius": 10,
    "icon_size": 24,
}

# 间距配置
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32,
}


class ThemeManager:
    """Theme manager for handling light/dark themes."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.is_dark_mode = False
        self.current_colors = COLORS
        
    def toggle_theme(self):
        """Toggle between light and dark theme."""
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()
        return self.is_dark_mode
        
    def set_theme(self, dark_mode: bool):
        """Set theme mode."""
        self.is_dark_mode = dark_mode
        self.apply_theme()
        
    def apply_theme(self):
        """Apply current theme to page."""
        if self.is_dark_mode:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.current_colors = DARK_COLORS
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.current_colors = COLORS
            
        self.page.theme = ft.Theme(
            color_scheme_seed=self.current_colors["primary"],
            visual_density=ft.VisualDensity.COMFORTABLE,
            font_family="Microsoft YaHei",
        )
        self.page.update()
        
    def get_color(self, color_name: str) -> str:
        """Get color by name."""
        return self.current_colors.get(color_name, COLORS.get(color_name))
        
    def get_theme_info(self) -> Dict[str, Any]:
        """Get current theme information."""
        return {
            "is_dark_mode": self.is_dark_mode,
            "theme_mode": "dark" if self.is_dark_mode else "light",
            "primary_color": self.current_colors["primary"],
        }


def get_theme():
    """Get Flet theme configuration."""
    return ft.Theme(
        color_scheme_seed=COLORS["primary"],
        visual_density=ft.VisualDensity.COMFORTABLE,
        font_family="Microsoft YaHei",
    )


def get_dark_theme():
    """Get dark theme configuration."""
    return ft.Theme(
        color_scheme_seed=DARK_COLORS["primary"],
        visual_density=ft.VisualDensity.COMFORTABLE,
        font_family="Microsoft YaHei",
    )


def apply_theme(page: ft.Page, dark_mode: bool = False):
    """Apply theme to page."""
    if dark_mode:
        page.theme_mode = ft.ThemeMode.DARK
        page.theme = get_dark_theme()
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
        page.theme = get_theme()
    page.update()