"""Image tiling tab."""
import flet as ft


class TileTab:
    """Tab for image tiling."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        
    def build(self):
        """Build the tab content."""
        return ft.Container(
            content=ft.Column([
                # 输入文件选择
                self._create_input_section(),
                # 切片参数
                self._create_params_section(),
                # 预览区域
                self._create_preview_section(),
                # 操作按钮
                self._create_action_section(),
            ], spacing=15, scroll=ft.ScrollMode.AUTO),
            padding=20,
        )
        
    def _create_input_section(self):
        """Create input section."""
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("输入文件", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Row([
                        ft.TextField(
                            label="输入图片",
                            hint_text="选择大图文件",
                            expand=True,
                            read_only=True,
                        ),
                        ft.ElevatedButton(
                            "浏览...",
                            icon=ft.Icons.FOLDER_OPEN,
                            on_click=self._select_input_file,
                        ),
                    ]),
                ], spacing=10),
                padding=20,
            )
        )
        
    def _create_params_section(self):
        """Create parameters section."""
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("切片参数", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Row([
                        ft.Text("切片宽度:", width=100),
                        ft.TextField(
                            value="256",
                            width=100,
                            text_align=ft.TextAlign.RIGHT,
                        ),
                        ft.Text("像素"),
                    ]),
                    ft.Row([
                        ft.Text("切片高度:", width=100),
                        ft.TextField(
                            value="256",
                            width=100,
                            text_align=ft.TextAlign.RIGHT,
                        ),
                        ft.Text("像素"),
                    ]),
                    ft.Row([
                        ft.Text("重叠像素:", width=100),
                        ft.TextField(
                            value="0",
                            width=100,
                            text_align=ft.TextAlign.RIGHT,
                        ),
                        ft.Text("像素"),
                    ]),
                    ft.Row([
                        ft.Text("输出格式:", width=100),
                        ft.Dropdown(
                            width=150,
                            options=[
                                ft.dropdown.Option("png"),
                                ft.dropdown.Option("jpg"),
                                ft.dropdown.Option("webp"),
                            ],
                            value="png",
                        ),
                    ]),
                ], spacing=10),
                padding=20,
            )
        )
        
    def _create_preview_section(self):
        """Create preview section."""
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("切片预览", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("请先选择输入文件", color=ft.Colors.GREY_500),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        height=300,
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=10,
                        alignment=ft.Alignment.CENTER,
                    ),
                ], spacing=10),
                padding=20,
            )
        )
        
    def _create_action_section(self):
        """Create action section."""
        return ft.Row([
            ft.ElevatedButton(
                "开始切片",
                icon=ft.Icons.PLAY_ARROW,
                on_click=self._start_tiling,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.AMBER,
                    color=ft.Colors.WHITE,
                ),
            ),
            ft.OutlinedButton(
                "重置",
                icon=ft.Icons.REFRESH,
                on_click=self._reset_params,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER)
        
    def _select_input_file(self, e):
        """Handle input file selection."""
        # TODO: 实现文件选择
        pass
        
    def _start_tiling(self, e):
        """Start tiling process."""
        # TODO: 实现切片逻辑
        pass
        
    def _reset_params(self, e):
        """Reset parameters."""
        # TODO: 实现参数重置
        pass