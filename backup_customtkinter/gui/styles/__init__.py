"""GUI styles and themes."""
from gui.styles.theme import COLORS, FONTS, SIZES, apply_theme

# 导入现代主题
from gui.styles.theme_modern import (
    COLORS as MODERN_COLORS,
    FONTS as MODERN_FONTS,
    SPACING,
    SIZES as MODERN_SIZES,
    ICONS,
    ANIMATION,
    SHADOWS,
    get_colors,
    get_font,
    apply_theme as apply_modern_theme,
    get_button_style,
    get_input_style,
    get_card_style,
    create_button,
    create_entry,
    create_label,
    create_card,
    create_separator,
    create_form_row,
)

__all__ = [
    "COLORS", "FONTS", "SIZES", "apply_theme",
    "MODERN_COLORS", "MODERN_FONTS", "MODERN_SIZES",
    "SPACING", "ICONS", "ANIMATION", "SHADOWS",
    "get_colors", "get_font", "apply_modern_theme",
    "get_button_style", "get_input_style", "get_card_style",
    "create_button", "create_entry", "create_label",
    "create_card", "create_separator", "create_form_row",
]
