"""File selector widget."""
import flet as ft
from typing import Callable, Optional, List


class FileSelector:
    """File selector widget."""
    
    def __init__(
        self,
        page: ft.Page,
        mode: str = "file",  # file, directory, save
        label_text: str = "选择文件:",
        file_types: Optional[List[dict]] = None,
        on_change: Optional[Callable[[str], None]] = None,
    ):
        self.page = page
        self.mode = mode
        self.label_text = label_text
        self.file_types = file_types or []
        self.on_change = on_change
        self.file_path = ""
        self.path_field = None
        
    def build(self):
        """Build the widget."""
        self.path_field = ft.TextField(
            label=self.label_text,
            read_only=True,
            expand=True,
        )
        
        browse_button = ft.ElevatedButton(
            "浏览...",
            icon=ft.Icons.FOLDER_OPEN,
            on_click=self._on_browse,
        )
        
        return ft.Row([
            self.path_field,
            browse_button,
        ], alignment=ft.MainAxisAlignment.START)
        
    async def _on_browse(self, e):
        """Handle browse button click."""
        if self.mode == "file":
            file_picker = ft.FilePicker(
                on_result=self._on_file_picked,
            )
            self.page.overlay.append(file_picker)
            self.page.update()
            await file_picker.pick_files()
        elif self.mode == "directory":
            dir_picker = ft.FilePicker(
                on_result=self._on_dir_picked,
            )
            self.page.overlay.append(dir_picker)
            self.page.update()
            await dir_picker.get_directory_path()
        elif self.mode == "save":
            save_picker = ft.FilePicker(
                on_result=self._on_save_picked,
            )
            self.page.overlay.append(save_picker)
            self.page.update()
            await save_picker.save_file()
            
    def _on_file_picked(self, e):
        """Handle file picked."""
        if e.files:
            self.file_path = e.files[0].path
            self.path_field.value = self.file_path
            self.page.update()
            if self.on_change:
                self.on_change(self.file_path)
                
    def _on_dir_picked(self, e):
        """Handle directory picked."""
        if e.path:
            self.file_path = e.path
            self.path_field.value = self.file_path
            self.page.update()
            if self.on_change:
                self.on_change(self.file_path)
                
    def _on_save_picked(self, e):
        """Handle save picked."""
        if e.path:
            self.file_path = e.path
            self.path_field.value = self.file_path
            self.page.update()
            if self.on_change:
                self.on_change(self.file_path)