"""Drop zone widget."""
import flet as ft
from typing import Callable, Optional, List


class DropZone:
    """Drop zone widget for drag and drop file selection."""
    
    def __init__(
        self,
        page: ft.Page,
        on_files_dropped: Optional[Callable[[List[str]], None]] = None,
        accept_multiple: bool = True,
        accept_folders: bool = False,
    ):
        self.page = page
        self.on_files_dropped = on_files_dropped
        self.accept_multiple = accept_multiple
        self.accept_folders = accept_folders
        self.files: List[str] = []
        self.files_text = None
        
    def build(self):
        """Build the widget."""
        self.files_text = ft.Text(
            "拖放文件到这里或点击选择",
            color=ft.Colors.GREY_500,
            text_align=ft.TextAlign.CENTER,
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Icon(
                    ft.Icons.CLOUD_UPLOAD,
                    size=48,
                    color=ft.Colors.AMBER,
                ),
                self.files_text,
                ft.ElevatedButton(
                    "选择文件",
                    icon=ft.Icons.FOLDER_OPEN,
                    on_click=self._on_select_files,
                ),
            ], 
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10),
            width=400,
            height=200,
            border=ft.border.all(2, ft.Colors.AMBER),
            border_radius=10,
            bgcolor=ft.Colors.AMBER_50,
            alignment=ft.alignment.center,
            on_click=self._on_select_files,
        )
        
    async def _on_select_files(self, e):
        """Handle file selection."""
        file_picker = ft.FilePicker(
            on_result=self._on_files_picked,
        )
        self.page.overlay.append(file_picker)
        self.page.update()
        
        if self.accept_folders:
            await file_picker.get_directory_path()
        else:
            await file_picker.pick_files(
                allow_multiple=self.accept_multiple,
            )
            
    def _on_files_picked(self, e):
        """Handle files picked."""
        if e.files:
            self.files = [f.path for f in e.files]
            if self.files_text:
                if len(self.files) == 1:
                    self.files_text.value = f"已选择: {self.files[0]}"
                else:
                    self.files_text.value = f"已选择 {len(self.files)} 个文件"
                self.files_text.color = ft.Colors.GREEN
                self.page.update()
            
            if self.on_files_dropped:
                self.on_files_dropped(self.files)
                
    def clear(self):
        """Clear selected files."""
        self.files = []
        if self.files_text:
            self.files_text.value = "拖放文件到这里或点击选择"
            self.files_text.color = ft.Colors.GREY_500
            self.page.update()