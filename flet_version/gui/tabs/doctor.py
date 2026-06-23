"""Environment diagnosis tab."""
import flet as ft


class DoctorTab:
    """Tab for environment diagnosis."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        
    def build(self):
        """Build the tab content."""
        return ft.Container(
            content=ft.Column([
                # 诊断项目
                self._create_diagnosis_section(),
                # 诊断结果
                self._create_result_section(),
                # 操作按钮
                self._create_action_section(),
            ], spacing=15, scroll=ft.ScrollMode.AUTO),
            padding=20,
        )
        
    def _create_diagnosis_section(self):
        """Create diagnosis section."""
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("环境诊断", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    # 诊断项目列表
                    ft.Column([
                        self._create_diagnosis_item("Python 版本", "检查 Python 版本是否符合要求"),
                        self._create_diagnosis_item("Pillow 库", "检查 Pillow 是否安装及版本"),
                        self._create_diagnosis_item("pyvips 库", "检查 pyvips 是否安装及版本"),
                        self._create_diagnosis_item("libvips 库", "检查 libvips 是否安装"),
                        self._create_diagnosis_item("系统环境", "检查系统环境配置"),
                    ], spacing=5),
                ], spacing=10),
                padding=20,
            )
        )
        
    def _create_diagnosis_item(self, title: str, description: str):
        """Create a diagnosis item."""
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREY_400, size=20),
                ft.Column([
                    ft.Text(title, weight=ft.FontWeight.BOLD),
                    ft.Text(description, size=12, color=ft.Colors.GREY_600),
                ], spacing=2, expand=True),
            ], spacing=10),
            padding=10,
            border_radius=8,
            bgcolor=ft.Colors.GREY_50,
        )
        
    def _create_result_section(self):
        """Create result section."""
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("诊断结果", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("点击开始诊断按钮进行环境检查", color=ft.Colors.GREY_500),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        height=200,
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=10,
                        padding=10,
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
                "开始诊断",
                icon=ft.Icons.PLAY_ARROW,
                on_click=self._start_diagnosis,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.AMBER,
                    color=ft.Colors.WHITE,
                ),
            ),
            ft.OutlinedButton(
                "修复问题",
                icon=ft.Icons.BUILD,
                on_click=self._fix_issues,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER)
        
    def _start_diagnosis(self, e):
        """Start diagnosis."""
        # TODO: 实现诊断逻辑
        pass
        
    def _fix_issues(self, e):
        """Fix issues."""
        # TODO: 实现修复逻辑
        pass