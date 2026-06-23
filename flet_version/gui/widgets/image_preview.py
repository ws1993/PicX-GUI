"""Image preview widget."""
import flet as ft


class ImagePreview:
    """Image preview widget."""
    
    def __init__(
        self,
        page: ft.Page,
        image_path: str = None,
        width: int = 300,
        height: int = 300,
    ):
        self.page = page
        self.image_path = image_path
        self.width = width
        self.height = height
        self.image_control = None
        self.info_text = None
        
    def build(self):
        """Build the widget."""
        self.image_control = ft.Image(
            src=self.image_path,
            width=self.width,
            height=self.height,
            fit=ft.ImageFit.CONTAIN,
            border_radius=10,
        )
        
        self.info_text = ft.Text(
            "未选择图片",
            size=12,
            color=ft.Colors.GREY_500,
            text_align=ft.TextAlign.CENTER,
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=self.image_control if self.image_path else ft.Icon(
                        ft.Icons.IMAGE,
                        size=64,
                        color=ft.Colors.GREY_300,
                    ),
                    width=self.width,
                    height=self.height,
                    bgcolor=ft.Colors.GREY_100,
                    border_radius=10,
                    alignment=ft.alignment.center,
                ),
                self.info_text,
            ], 
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10),
            padding=10,
        )
        
    def set_image(self, image_path: str):
        """Set image path."""
        self.image_path = image_path
        if self.image_control:
            self.image_control.src = image_path
        if self.info_text:
            self.info_text.value = image_path.split("\\")[-1] if "\\" in image_path else image_path.split("/")[-1]
            self.info_text.color = ft.Colors.GREY_700
        self.page.update()
        
    def clear(self):
        """Clear image."""
        self.image_path = None
        if self.image_control:
            self.image_control.src = None
        if self.info_text:
            self.info_text.value = "未选择图片"
            self.info_text.color = ft.Colors.GREY_500
        self.page.update()
        
    def get_image_info(self):
        """Get image information."""
        if self.image_path:
            return {
                "path": self.image_path,
                "filename": self.image_path.split("\\")[-1] if "\\" in self.image_path else self.image_path.split("/")[-1],
            }
        return None