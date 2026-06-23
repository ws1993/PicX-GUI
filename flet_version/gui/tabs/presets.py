"""Presets management tab."""
import flet as ft


class PresetsTab:
    """Tab for presets management."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        
    def build(self):
        """Build the tab content."""
        return ft.Container(
            content=ft.Column([
                # 预设列表
                self._create_presets_section(),
                # 预设编辑
                self._create_edit_section(),
                # 操作按钮
                self._create_action_section(),
            ], spacing=15, scroll=ft.ScrollMode.AUTO),
            padding=20,
        )
        
    def _create_presets_section(self):
        """Create presets section."""
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("预设列表", size=16, weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton(
                            "新建预设",
                            icon=ft.Icons.ADD,
                            on_click=self._create_preset,
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(),
                    # 预设列表
                    ft.Column([
                        self._create_preset_item("Web 优化", "WebP, 质量 82, 最大宽度 1920"),
                        self._create_preset_item("博客图片", "WebP, 质量 78, 最大宽度 1600"),
                        self._create_preset_item("头像", "WebP, 质量 85, 256x256"),
                        self._create_preset_item("无损压缩", "PNG, 质量 100"),
                    ], spacing=5),
                ], spacing=10),
                padding=20,
            )
        )
        
    def _create_preset_item(self, name: str, description: str):
        """Create a preset item."""
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.SETTINGS, color=ft.Colors.AMBER, size=20),
                ft.Column([
                    ft.Text(name, weight=ft.FontWeight.BOLD),
                    ft.Text(description, size=12, color=ft.Colors.GREY_600),
                ], spacing=2, expand=True),
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_size=16,
                        tooltip="编辑",
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_size=16,
                        tooltip="删除",
                        icon_color=ft.Colors.RED,
                    ),
                ], spacing=0),
            ], spacing=10),
            padding=10,
            border_radius=8,
            bgcolor=ft.Colors.GREY_50,
        )
        
    def _create_edit_section(self):
        """Create edit section."""
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("编辑预设", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.TextField(
                        label="预设名称",
                        hint_text="输入预设名称",
                    ),
                    ft.Row([
                        ft.Text("输出格式:", width=100),
                        ft.Dropdown(
                            width=150,
                            options=[
                                ft.dropdown.Option("webp"),
                                ft.dropdown.Option("jpg"),
                                ft.dropdown.Option("png"),
                                ft.dropdown.Option("avif"),
                            ],
                            value="webp",
                        ),
                    ]),
                    ft.Row([
                        ft.Text("质量:", width=100),
                        ft.Slider(
                            min=1,
                            max=100,
                            value=82,
                            divisions=99,
                            label="{value}%",
                            expand=True,
                        ),
                    ]),
                    ft.TextField(
                        label="最大宽度",
                        hint_text="像素",
                        value="1920",
                    ),
                    ft.TextField(
                        label="最大高度",
                        hint_text="像素（可选）",
                    ),
                ], spacing=10),
                padding=20,
            )
        )
        
    def _create_action_section(self):
        """Create action section."""
        return ft.Row([
            ft.ElevatedButton(
                "保存预设",
                icon=ft.Icons.SAVE,
                on_click=self._save_preset,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.AMBER,
                    color=ft.Colors.WHITE,
                ),
            ),
            ft.OutlinedButton(
                "导入预设",
                icon=ft.Icons.UPLOAD,
                on_click=self._import_preset,
            ),
            ft.OutlinedButton(
                "导出预设",
                icon=ft.Icons.DOWNLOAD,
                on_click=self._export_preset,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER)
        
    def _create_preset(self, e):
        """Create new preset."""
        # TODO: 实现新建预设
        pass
        
    def _save_preset(self, e):
        """Save preset."""
        # TODO: 实现保存预设
        pass
        
    def _import_preset(self, e):
        """Import preset."""
        # TODO: 实现导入预设
        pass
        
    def _export_preset(self, e):
        """Export preset."""
        # TODO: 实现导出预设
        pass