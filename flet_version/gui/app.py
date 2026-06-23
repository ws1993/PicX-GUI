"""Main application class."""
import flet as ft
from gui.tabs.single_image import SingleImageTab
from gui.tabs.batch import BatchTab
from gui.tabs.tile import TileTab
from gui.tabs.doctor import DoctorTab
from gui.tabs.presets import PresetsTab
from gui.styles.theme import ThemeManager
from gui.locales import LocaleManager, get_text
from gui.utils.keyboard_shortcuts import create_default_shortcuts


class PicXApp:
    """PicX GUI Application."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.status_text = None
        self.theme_manager = ThemeManager(page)
        self.locale_manager = LocaleManager("zh_CN")
        self.keyboard_shortcuts = create_default_shortcuts(page)
        
    def build(self):
        """Build the application UI."""
        # 应用主题
        self.theme_manager.apply_theme()
        
        # 创建标签页
        self.tabs = ft.Tabs(
            length=5,
            selected_index=0,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label=get_text("tab_single_image"), icon=ft.Icons.IMAGE_OUTLINED),
                            ft.Tab(label=get_text("tab_batch"), icon=ft.Icons.COLLECTIONS_OUTLINED),
                            ft.Tab(label=get_text("tab_tile"), icon=ft.Icons.GRID_ON_OUTLINED),
                            ft.Tab(label=get_text("tab_doctor"), icon=ft.Icons.BUILD_OUTLINED),
                            ft.Tab(label=get_text("tab_presets"), icon=ft.Icons.SETTINGS_OUTLINED),
                        ]
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            SingleImageTab(self.page).build(),
                            BatchTab(self.page).build(),
                            TileTab(self.page).build(),
                            DoctorTab(self.page).build(),
                            PresetsTab(self.page).build(),
                        ],
                    ),
                ],
            ),
            on_change=self._on_tab_change,
        )
        
        # 创建状态栏
        self.status_text = ft.Text(get_text("status_ready"), size=12, color=ft.Colors.GREY_600)
        
        # 布局
        self.page.add(
            ft.Column([
                self._create_header(),
                ft.Container(
                    content=self.tabs,
                    expand=True,
                    padding=ft.Padding.all(10),
                ),
                self._create_status_bar(),
            ], expand=True)
        )
        
    def _create_header(self):
        """Create application header."""
        # 主题切换按钮
        theme_icon = ft.Icons.DARK_MODE if self.theme_manager.is_dark_mode else ft.Icons.LIGHT_MODE
        theme_button = ft.IconButton(
            icon=theme_icon,
            icon_color=ft.Colors.GREY_400,
            tooltip="切换主题",
            on_click=self._toggle_theme,
        )
        
        # 语言切换按钮
        language_button = ft.IconButton(
            icon=ft.Icons.LANGUAGE,
            icon_color=ft.Colors.GREY_400,
            tooltip="切换语言",
            on_click=self._toggle_language,
        )
        
        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Icon(ft.Icons.IMAGE, color=ft.Colors.AMBER, size=32),
                    ft.Column([
                        ft.Text(
                            "PicX",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                        ft.Text(
                            get_text("app_name"),
                            size=14,
                            color=ft.Colors.GREY_400,
                        ),
                    ], spacing=2, alignment=ft.MainAxisAlignment.CENTER),
                ], spacing=10),
                ft.Row([
                    language_button,
                    theme_button,
                    ft.IconButton(
                        icon=ft.Icons.SETTINGS_OUTLINED,
                        icon_color=ft.Colors.GREY_400,
                        tooltip="设置",
                    ),
                    ft.IconButton(
                        icon=ft.Icons.HELP_OUTLINE,
                        icon_color=ft.Colors.GREY_400,
                        tooltip="帮助",
                    ),
                ]),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=ft.Colors.GREY_900,
            padding=ft.Padding(20, 15, 20, 15),
        )
        
    def _create_status_bar(self):
        """Create status bar."""
        return ft.Container(
            content=ft.Row([
                self.status_text,
                ft.Text("v2.0.0", size=12, color=ft.Colors.GREY_500),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=ft.Colors.GREY_100,
            padding=ft.Padding(15, 8, 15, 8),
        )
        
    def _on_tab_change(self, e):
        """Handle tab change."""
        tab_names = [
            get_text("tab_single_image"),
            get_text("tab_batch"),
            get_text("tab_tile"),
            get_text("tab_doctor"),
            get_text("tab_presets"),
        ]
        selected_index = e.control.selected_index
        if selected_index < len(tab_names):
            self.update_status(f"已切换到 {tab_names[selected_index]}")
            
    def _toggle_theme(self, e):
        """Toggle theme between light and dark."""
        is_dark = self.theme_manager.toggle_theme()
        theme_name = "深色" if is_dark else "浅色"
        self.update_status(f"已切换到{theme_name}主题")
        
    def _toggle_language(self, e):
        """Toggle language between Chinese and English."""
        current_lang = self.locale_manager.language
        new_lang = "en_US" if current_lang == "zh_CN" else "zh_CN"
        self.locale_manager.set_language(new_lang)
        lang_name = self.locale_manager.get_language_name(new_lang)
        self.update_status(f"已切换到{lang_name}")
        
    def update_status(self, text: str):
        """Update status bar text."""
        if self.status_text:
            self.status_text.value = text
            self.page.update()