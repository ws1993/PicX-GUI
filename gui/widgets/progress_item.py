"""Progress item widget."""
import flet as ft


class ProgressItem:
    """Progress item widget for displaying task progress."""
    
    def __init__(
        self,
        page: ft.Page,
        task_name: str = "任务",
        show_cancel: bool = True,
        on_cancel=None,
    ):
        self.page = page
        self.task_name = task_name
        self.show_cancel = show_cancel
        self.on_cancel = on_cancel
        self.progress_bar = None
        self.status_text = None
        self.progress_text = None
        
    def build(self):
        """Build the widget."""
        self.progress_bar = ft.ProgressBar(
            value=0,
            color=ft.Colors.AMBER,
            bgcolor=ft.Colors.GREY_200,
        )
        
        self.status_text = ft.Text(
            "等待中",
            size=12,
            color=ft.Colors.GREY_600,
        )
        
        self.progress_text = ft.Text(
            "0%",
            size=12,
            weight=ft.FontWeight.BOLD,
        )
        
        cancel_button = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_size=16,
            tooltip="取消",
            on_click=self._on_cancel_click,
            visible=self.show_cancel,
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(self.task_name, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        self.status_text,
                        self.progress_text,
                        cancel_button,
                    ], spacing=5),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.progress_bar,
            ], spacing=5),
            padding=10,
            border_radius=8,
            bgcolor=ft.Colors.GREY_50,
        )
        
    def update_progress(self, value: float, status: str = None):
        """Update progress value."""
        if self.progress_bar:
            self.progress_bar.value = value
        if self.progress_text:
            self.progress_text.value = f"{int(value * 100)}%"
        if status and self.status_text:
            self.status_text.value = status
        self.page.update()
        
    def set_status(self, status: str, color: str = None):
        """Set status text."""
        if self.status_text:
            self.status_text.value = status
            if color:
                self.status_text.color = color
            self.page.update()
            
    def set_completed(self):
        """Set task as completed."""
        self.update_progress(1.0, "已完成")
        if self.status_text:
            self.status_text.color = ft.Colors.GREEN
        if self.progress_bar:
            self.progress_bar.color = ft.Colors.GREEN
        self.page.update()
        
    def set_error(self, error_message: str):
        """Set task as error."""
        self.set_status(f"错误: {error_message}", ft.Colors.RED)
        if self.progress_bar:
            self.progress_bar.color = ft.Colors.RED
        self.page.update()
        
    def _on_cancel_click(self, e):
        """Handle cancel button click."""
        if self.on_cancel:
            self.on_cancel()