"""Modern theme configuration for PicX GUI."""
import customtkinter as ctk


# Color scheme - Modern warm theme
COLORS = {
    "primary": "#C8853F",
    "primary_hover": "#A86B2C",
    "primary_light": "#E8B882",
    "background": "#F6F1E8",
    "surface": "#FBF7EF",
    "surface_light": "#FFFFFF",
    "surface_dark": "#F0E8D8",
    "border": "#E2D9C8",
    "border_light": "#EDE6D8",
    "text": "#1F2421",
    "text_secondary": "#4A4A42",
    "text_muted": "#8A8A80",
    "accent_tint": "#F0E3D0",
    "dark_block": "#2A2723",
    
    # Status colors
    "success": "#4CAF50",
    "success_light": "#E8F5E9",
    "warning": "#FF9800",
    "warning_light": "#FFF3E0",
    "error": "#F44336",
    "error_light": "#FFEBEE",
    "info": "#2196F3",
    "info_light": "#E3F2FD",
}

# Font configuration
FONTS = {
    "heading": ("DM Serif Display", 24, "bold"),
    "subheading": ("DM Serif Display", 18, "bold"),
    "title": ("DM Serif Display", 16, "bold"),
    "body": ("Inter", 11),
    "body_bold": ("Inter", 11, "bold"),
    "small": ("Inter", 10),
    "small_bold": ("Inter", 10, "bold"),
    "button": ("Inter", 11, "bold"),
    "button_large": ("Inter", 13, "bold"),
    "mono": ("Consolas", 11),
}

# Spacing configuration
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 12,
    "lg": 16,
    "xl": 20,
    "xxl": 24,
    "xxxl": 32,
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
    "button_height_large": 44,
    "entry_height": 32,
    "corner_radius": 8,
    "corner_radius_large": 12,
    "border_width": 1,
}

# Icon characters (using Unicode)
ICONS = {
    "folder": "📁",
    "file": "📄",
    "image": "🖼️",
    "settings": "⚙️",
    "check": "✓",
    "cross": "✗",
    "warning": "⚠",
    "info": "ℹ",
    "refresh": "🔄",
    "copy": "📋",
    "save": "💾",
    "delete": "🗑️",
    "edit": "✏️",
    "plus": "+",
    "minus": "-",
    "arrow_up": "↑",
    "arrow_down": "↓",
    "arrow_left": "←",
    "arrow_right": "→",
}

# Animation configuration
ANIMATION = {
    "fast": 100,
    "normal": 200,
    "slow": 300,
}

# Shadow configuration
SHADOWS = {
    "small": "0 1px 2px rgba(0,0,0,0.1)",
    "medium": "0 2px 4px rgba(0,0,0,0.1)",
    "large": "0 4px 8px rgba(0,0,0,0.15)",
}


def get_colors(mode="light"):
    """
    Get color scheme for specified mode.
    
    Args:
        mode: "light" or "dark"
        
    Returns:
        Color dictionary
    """
    if mode == "dark":
        dark_colors = COLORS.copy()
        dark_colors.update({
            "background": "#1A1A1A",
            "surface": "#2D2D2D",
            "surface_light": "#3D3D3D",
            "surface_dark": "#252525",
            "border": "#404040",
            "border_light": "#4A4A4A",
            "text": "#FFFFFF",
            "text_secondary": "#E0E0E0",
            "text_muted": "#888888",
            "accent_tint": "#3D3020",
            "dark_block": "#1A1A1A",
        })
        return dark_colors
    return COLORS


def get_font(size="body", bold=False):
    """
    Get font configuration.
    
    Args:
        size: Font size name
        bold: Whether to use bold
        
    Returns:
        Font tuple
    """
    if bold:
        return FONTS.get(f"{size}_bold", FONTS["body_bold"])
    return FONTS.get(size, FONTS["body"])


def apply_theme(mode="light"):
    """
    Apply modern theme to CustomTkinter.
    
    Args:
        mode: "light" or "dark"
    """
    ctk.set_appearance_mode(mode)
    ctk.set_default_color_theme("blue")


def get_button_style(style="primary"):
    """
    Get button style configuration.
    
    Args:
        style: Button style name
        
    Returns:
        Style dictionary
    """
    styles = {
        "primary": {
            "fg_color": COLORS["primary"],
            "hover_color": COLORS["primary_hover"],
            "text_color": "white",
            "font": FONTS["button"],
            "corner_radius": SIZES["corner_radius"],
            "height": SIZES["button_height"],
        },
        "secondary": {
            "fg_color": COLORS["surface_dark"],
            "hover_color": COLORS["border"],
            "text_color": COLORS["text"],
            "font": FONTS["button"],
            "corner_radius": SIZES["corner_radius"],
            "height": SIZES["button_height"],
        },
        "success": {
            "fg_color": COLORS["success"],
            "hover_color": "#43A047",
            "text_color": "white",
            "font": FONTS["button"],
            "corner_radius": SIZES["corner_radius"],
            "height": SIZES["button_height"],
        },
        "danger": {
            "fg_color": COLORS["error"],
            "hover_color": "#E53935",
            "text_color": "white",
            "font": FONTS["button"],
            "corner_radius": SIZES["corner_radius"],
            "height": SIZES["button_height"],
        },
    }
    return styles.get(style, styles["primary"])


def get_input_style():
    """
    Get input style configuration.
    
    Returns:
        Style dictionary
    """
    return {
        "fg_color": COLORS["surface_light"],
        "border_color": COLORS["border"],
        "text_color": COLORS["text"],
        "placeholder_text_color": COLORS["text_muted"],
        "font": FONTS["body"],
        "corner_radius": SIZES["corner_radius"],
        "height": SIZES["entry_height"],
        "border_width": SIZES["border_width"],
    }


def get_card_style():
    """
    Get card style configuration.
    
    Returns:
        Style dictionary
    """
    return {
        "fg_color": COLORS["surface"],
        "corner_radius": SIZES["corner_radius"],
        "border_width": SIZES["border_width"],
        "border_color": COLORS["border"],
    }


def create_button(master, text, style="primary", command=None, **kwargs):
    """
    Create styled button.
    
    Args:
        master: Parent widget
        text: Button text
        style: Button style
        command: Click handler
        **kwargs: Additional options
        
    Returns:
        CTkButton instance
    """
    btn_style = get_button_style(style)
    btn_style.update(kwargs)
    return ctk.CTkButton(master, text=text, command=command, **btn_style)


def create_entry(master, placeholder="", **kwargs):
    """
    Create styled entry.
    
    Args:
        master: Parent widget
        placeholder: Placeholder text
        **kwargs: Additional options
        
    Returns:
        CTkEntry instance
    """
    entry_style = get_input_style()
    entry_style.update(kwargs)
    return ctk.CTkEntry(master, placeholder_text=placeholder, **entry_style)


def create_label(master, text, size="body", **kwargs):
    """
    Create styled label.
    
    Args:
        master: Parent widget
        text: Label text
        size: Font size
        **kwargs: Additional options
        
    Returns:
        CTkLabel instance
    """
    font = FONTS.get(size, FONTS["body"])
    return ctk.CTkLabel(master, text=text, font=font, text_color=COLORS["text"], **kwargs)


def create_card(master, **kwargs):
    """
    Create card frame.
    
    Args:
        master: Parent widget
        **kwargs: Additional options
        
    Returns:
        CTkFrame instance
    """
    card_style = get_card_style()
    card_style.update(kwargs)
    return ctk.CTkFrame(master, **card_style)


def create_separator(master, **kwargs):
    """
    Create separator line.
    
    Args:
        master: Parent widget
        **kwargs: Additional options
        
    Returns:
        CTkFrame instance (thin line)
    """
    return ctk.CTkFrame(master, height=1, fg_color=COLORS["border"], **kwargs)


def create_form_row(master, label_text, widget_factory, row=0, **kwargs):
    """
    Create form row with label and widget.
    
    Args:
        master: Parent widget
        label_text: Label text
        widget_factory: Function to create the widget
        row: Grid row
        **kwargs: Additional widget options
        
    Returns:
        Tuple of (label, widget)
    """
    label = create_label(master, label_text)
    label.grid(row=row, column=0, sticky="w", padx=SPACING["md"], pady=SPACING["sm"])
    
    widget = widget_factory(master, **kwargs)
    widget.grid(row=row, column=1, sticky="ew", padx=SPACING["md"], pady=SPACING["sm"])
    
    return label, widget
