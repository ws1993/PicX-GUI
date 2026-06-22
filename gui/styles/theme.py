"""Theme configuration for PicX GUI."""
import customtkinter as ctk

# Color scheme
COLORS = {
    "primary": "#C8853F",      # Amber accent
    "primary_hover": "#A86B2C",
    "background": "#F6F1E8",    # Warm paper
    "surface": "#FBF7EF",
    "surface_light": "#FFFFFF",
    "border": "#E2D9C8",
    "text": "#1F2421",
    "text_muted": "#8A8A80",
    "accent_tint": "#F0E3D0",
    "dark_block": "#2A2723",
    
    # Status colors
    "success": "#4CAF50",
    "warning": "#FF9800",
    "error": "#F44336",
    "info": "#2196F3",
}

# Font configuration
FONTS = {
    "heading": ("DM Serif Display", 24, "bold"),
    "subheading": ("DM Serif Display", 18, "bold"),
    "body": ("Inter", 11),
    "body_bold": ("Inter", 11, "bold"),
    "small": ("Inter", 10),
    "button": ("Inter", 11, "bold"),
}

# Size configuration
SIZES = {
    "window_width": 1200,
    "window_height": 800,
    "min_width": 900,
    "min_height": 600,
    "padding": 20,
    "padding_small": 10,
    "button_height": 36,
    "entry_height": 32,
    "corner_radius": 8,
}


def apply_theme(mode="light"):
    """
    Apply theme to CustomTkinter.
    
    Args:
        mode: "light" or "dark"
    """
    ctk.set_appearance_mode(mode)
    
    if mode == "dark":
        ctk.set_default_color_theme("blue")
    else:
        # Custom light theme with warm colors
        ctk.set_default_color_theme("blue")
