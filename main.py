"""PicX GUI - Flet version."""
import flet as ft
from gui.app import PicXApp


def main(page: ft.Page):
    """Main entry point."""
    # 配置窗口
    page.title = "PicX - 图片优化工具"
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 800
    page.window.min_height = 600
    
    # 设置主题
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.AMBER,
        visual_density=ft.VisualDensity.COMFORTABLE,
    )
    
    # 创建应用实例
    app = PicXApp(page)
    app.build()


if __name__ == "__main__":
    ft.app(target=main)