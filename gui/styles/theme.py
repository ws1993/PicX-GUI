"""Theme configuration for PicX GUI."""
import customtkinter as ctk
import os

# Color scheme - Optimized for better coordination and contrast
COLORS = {
    # Primary colors - warmer, more cohesive amber palette
    "primary": "#D4943A",      # Slightly warmer amber
    "primary_hover": "#C08430", # Darker hover state
    "primary_light": "#E8B882", # Lighter variant
    "primary_disabled": "#D4B896", # Disabled state
    
    # Background and surface colors - better hierarchy
    "background": "#F8F4EE",    # Lighter, more neutral background
    "surface": "#FDF9F3",      # Clean surface
    "surface_light": "#FFFFFF", # Pure white for cards
    "surface_dark": "#F0E8D8", # Slightly darker surface
    "border": "#E8E0D4",       # Softer border
    "border_light": "#F0E8DC", # Lighter border variant
    
    # Text colors - better contrast hierarchy
    "text": "#2D2A26",         # Darker for better contrast
    "text_secondary": "#5A5650", # Secondary text
    "text_muted": "#8A8478",   # Muted text
    "accent_tint": "#F5E6D0",  # Accent tint
    
    # Header background
    "header_bg": "#2A2723",
    
    # Status colors - more refined
    "success": "#4CAF50",
    "success_light": "#E8F5E9",
    "warning": "#FF9800",
    "warning_light": "#FFF3E0",
    "error": "#F44336",
    "error_light": "#FFEBEE",
    "info": "#2196F3",
    "info_light": "#E3F2FD",
}

# Font configuration - Improved for Chinese text and hierarchy
FONTS = {
    # Headings - using system fonts for better Chinese support
    "heading": ("Microsoft YaHei", 20, "bold"),  # Better Chinese support
    "subheading": ("Microsoft YaHei", 16, "bold"),
    "title": ("Microsoft YaHei", 14, "bold"),
    
    # Body text - clear hierarchy
    "body": ("Microsoft YaHei", 11),
    "body_bold": ("Microsoft YaHei", 11, "bold"),
    "small": ("Microsoft YaHei", 10),
    "small_bold": ("Microsoft YaHei", 10, "bold"),
    
    # Button text - consistent with body
    "button": ("Microsoft YaHei", 11, "bold"),
    "button_large": ("Microsoft YaHei", 13, "bold"),
    
    # Monospace for paths and technical info
    "mono": ("Consolas", 11),
}

# Spacing configuration - Unified spacing system
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 12,
    "lg": 16,
    "xl": 20,
    "xxl": 24,
    "xxxl": 32,
}

# Size configuration - Consistent sizing
SIZES = {
    "window_width": 1200,
    "window_height": 800,
    "min_width": 1000,  # Slightly larger minimum
    "min_height": 700,
    "padding": 20,
    "padding_small": 10,
    "button_height": 36,
    "button_height_large": 44,
    "entry_height": 32,
    "corner_radius": 8,
    "corner_radius_large": 12,
    "border_width": 1,
}


def apply_theme(mode="light"):
    """
    Apply theme to CustomTkinter.
    
    Args:
        mode: Only "light" is supported (dark mode removed)
    """
    # Always use light mode
    ctk.set_appearance_mode("light")
    
    # Use Breeze theme from CTkThemesPack
    theme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "themes", "breeze.json")
    if os.path.exists(theme_path):
        ctk.set_default_color_theme(theme_path)
    else:
        # Fallback to default blue theme
        ctk.set_default_color_theme("blue")
