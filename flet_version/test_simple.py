"""Simple test for PicX GUI - Flet version."""
import flet as ft


def main(page: ft.Page):
    """Main entry point."""
    page.title = "PicX - 图片优化工具"
    page.window.width = 1200
    page.window.height = 800
    
    # 设置主题
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.AMBER,
        visual_density=ft.VisualDensity.COMFORTABLE,
    )
    
    # 创建简单的UI
    page.add(
        ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.IMAGE, color=ft.Colors.AMBER, size=32),
                    ft.Text("PicX", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ], spacing=10),
                bgcolor=ft.Colors.GREY_900,
                padding=20,
            ),
            ft.Container(
                content=ft.Tabs(
                    length=2,
                    selected_index=0,
                    expand=True,
                    content=ft.Column(
                        expand=True,
                        controls=[
                            ft.TabBar(
                                tabs=[
                                    ft.Tab(label="单图压缩", icon=ft.Icons.IMAGE_OUTLINED),
                                    ft.Tab(label="批量处理", icon=ft.Icons.COLLECTIONS_OUTLINED),
                                ]
                            ),
                            ft.TabBarView(
                                expand=True,
                                controls=[
                                    ft.Container(
                                        alignment=ft.Alignment.CENTER,
                                        content=ft.Text("单图压缩功能"),
                                    ),
                                    ft.Container(
                                        alignment=ft.Alignment.CENTER,
                                        content=ft.Text("批量处理功能"),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
                expand=True,
                padding=10,
            ),
            ft.Container(
                content=ft.Row([
                    ft.Text("就绪", size=12, color=ft.Colors.GREY_600),
                    ft.Text("v2.0.0", size=12, color=ft.Colors.GREY_500),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor=ft.Colors.GREY_100,
                padding=10,
            ),
        ], expand=True)
    )


if __name__ == "__main__":
    ft.app(target=main)