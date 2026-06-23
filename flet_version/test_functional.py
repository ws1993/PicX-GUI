"""Functional test for PicX GUI - Flet version."""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import flet as ft
from gui.tabs.single_image import SingleImageTab
from gui.tabs.batch import BatchTab


def main(page: ft.Page):
    """Main entry point."""
    page.title = "PicX - 功能测试"
    page.window.width = 1200
    page.window.height = 800
    
    # 设置主题
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.AMBER,
        visual_density=ft.VisualDensity.COMFORTABLE,
    )
    
    # 创建标签页
    tabs = ft.Tabs(
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
                        SingleImageTab(page).build(),
                        BatchTab(page).build(),
                    ],
                ),
            ],
        ),
    )
    
    # 布局
    page.add(
        ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.IMAGE, color=ft.Colors.AMBER, size=32),
                    ft.Text("PicX - 功能测试", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ], spacing=10),
                bgcolor=ft.Colors.GREY_900,
                padding=20,
            ),
            ft.Container(
                content=tabs,
                expand=True,
                padding=10,
            ),
            ft.Container(
                content=ft.Text("功能测试版本", size=12, color=ft.Colors.GREY_500),
                bgcolor=ft.Colors.GREY_100,
                padding=10,
            ),
        ], expand=True)
    )


if __name__ == "__main__":
    ft.app(target=main)