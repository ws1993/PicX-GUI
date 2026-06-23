"""Single image compression tab."""
import flet as ft
import os
import threading
from typing import Optional


class SingleImageTab:
    """Tab for single image compression."""
    
    # PicX presets
    PRESETS = {
        "Custom": None,
        "web": {"format": "webp", "quality": 82, "max_width": 1920},
        "blog": {"format": "webp", "quality": 78, "max_width": 1600},
        "avatar": {"format": "webp", "quality": 85, "max_width": 256, "max_height": 256},
        "lossless": {"format": "png", "quality": 100},
    }

    FORMATS = ["webp", "jpg", "png", "avif", "tiff"]
    BACKENDS = ["auto", "pillow", "pyvips"]
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.input_path = ""
        self.output_path = ""
        self.current_task = None
        
        # UI components
        self.input_field = None
        self.output_field = None
        self.preset_dropdown = None
        self.format_dropdown = None
        self.quality_slider = None
        self.quality_text = None
        self.max_width_field = None
        self.max_height_field = None
        self.backend_dropdown = None
        self.progress_bar = None
        self.status_text = None
        self.result_text = None
        
    def build(self):
        """Build the tab content."""
        return ft.Container(
            content=ft.Column([
                # 输入区域
                self._create_input_section(),
                # 参数配置区域
                self._create_params_section(),
                # 操作按钮区域
                self._create_action_section(),
                # 结果显示区域
                self._create_result_section(),
            ], spacing=15, scroll=ft.ScrollMode.AUTO),
            padding=20,
        )
        
    def _create_input_section(self):
        """Create input section."""
        # 输入文件选择
        self.input_field = ft.TextField(
            label="输入图片",
            hint_text="选择图片文件",
            expand=True,
            read_only=True,
        )
        
        # 输出路径选择
        self.output_field = ft.TextField(
            label="输出路径",
            hint_text="选择保存位置",
            expand=True,
            read_only=True,
        )
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("输入与输出", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    # 输入文件选择
                    ft.Row([
                        self.input_field,
                        ft.ElevatedButton(
                            "浏览...",
                            icon=ft.Icons.FOLDER_OPEN,
                            on_click=self._select_input_file,
                        ),
                    ]),
                    # 输出路径选择
                    ft.Row([
                        self.output_field,
                        ft.ElevatedButton(
                            "浏览...",
                            icon=ft.Icons.FOLDER_OPEN,
                            on_click=self._select_output_path,
                        ),
                    ]),
                ], spacing=10),
                padding=20,
            )
        )
        
    def _create_params_section(self):
        """Create parameters section."""
        # 预设选择
        self.preset_dropdown = ft.Dropdown(
            width=200,
            options=[ft.dropdown.Option(name) for name in self.PRESETS.keys()],
            value="Custom",
            on_select=self._on_preset_changed,
        )
        
        # 输出格式
        self.format_dropdown = ft.Dropdown(
            width=200,
            options=[ft.dropdown.Option(fmt) for fmt in self.FORMATS],
            value="webp",
        )
        
        # 质量滑块
        self.quality_slider = ft.Slider(
            min=1,
            max=100,
            value=82,
            divisions=99,
            label="{value}%",
            on_change=self._on_quality_changed,
        )
        
        self.quality_text = ft.Text("82%", width=50, weight=ft.FontWeight.BOLD)
        
        # 最大宽度
        self.max_width_field = ft.TextField(
            value="1920",
            width=100,
            text_align=ft.TextAlign.RIGHT,
            hint_text="留空保持原尺寸",
        )
        
        # 最大高度
        self.max_height_field = ft.TextField(
            value="",
            width=100,
            text_align=ft.TextAlign.RIGHT,
            hint_text="留空保持原尺寸",
        )
        
        # 后端选择
        self.backend_dropdown = ft.Dropdown(
            width=150,
            options=[ft.dropdown.Option(backend) for backend in self.BACKENDS],
            value="auto",
        )
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("压缩参数", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    # 预设选择
                    ft.Row([
                        ft.Text("预设:", width=100),
                        self.preset_dropdown,
                    ]),
                    # 输出格式
                    ft.Row([
                        ft.Text("输出格式:", width=100),
                        self.format_dropdown,
                    ]),
                    # 质量滑块
                    ft.Row([
                        ft.Text("质量:", width=100),
                        self.quality_slider,
                        self.quality_text,
                    ]),
                    # 最大宽度
                    ft.Row([
                        ft.Text("最大宽度:", width=100),
                        self.max_width_field,
                        ft.Text("像素"),
                    ]),
                    # 最大高度
                    ft.Row([
                        ft.Text("最大高度:", width=100),
                        self.max_height_field,
                        ft.Text("像素"),
                    ]),
                    # 后端选择
                    ft.Row([
                        ft.Text("处理后端:", width=100),
                        self.backend_dropdown,
                    ]),
                ], spacing=10),
                padding=20,
            )
        )
        
    def _create_action_section(self):
        """Create action section."""
        return ft.Row([
            ft.ElevatedButton(
                "开始压缩",
                icon=ft.Icons.PLAY_ARROW,
                on_click=self._start_compression,
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
            ft.OutlinedButton(
                "预览",
                icon=ft.Icons.IMAGE,
                on_click=self._preview_image,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER)
        
    def _create_result_section(self):
        """Create result section."""
        self.progress_bar = ft.ProgressBar(value=0, color=ft.Colors.AMBER)
        self.status_text = ft.Text("等待开始...", color=ft.Colors.GREY_500)
        self.result_text = ft.Text("")
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("处理结果", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    # 进度条
                    self.progress_bar,
                    # 状态信息
                    self.status_text,
                    # 结果信息
                    self.result_text,
                ], spacing=10),
                padding=20,
            )
        )
        
    def _select_input_file(self, e):
        """Handle input file selection."""
        file_picker = ft.FilePicker(
            on_result=self._on_input_file_picked,
        )
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(
            allowed_extensions=["png", "jpg", "jpeg", "webp", "avif", "tif", "tiff"],
        )
        
    def _on_input_file_picked(self, e):
        """Handle input file picked."""
        if e.files:
            self.input_path = e.files[0].path
            self.input_field.value = self.input_path
            self.page.update()
            
    def _select_output_path(self, e):
        """Handle output path selection."""
        file_picker = ft.FilePicker(
            on_result=self._on_output_path_picked,
        )
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.save_file(
            allowed_extensions=["webp", "jpg", "png", "avif", "tiff"],
        )
        
    def _on_output_path_picked(self, e):
        """Handle output path picked."""
        if e.path:
            self.output_path = e.path
            self.output_field.value = self.output_path
            self.page.update()
            
    def _on_preset_changed(self, e):
        """Handle preset change."""
        preset_name = e.control.value
        preset = self.PRESETS.get(preset_name)
        
        if preset:
            # 更新格式
            if "format" in preset:
                self.format_dropdown.value = preset["format"]
            
            # 更新质量
            if "quality" in preset:
                self.quality_slider.value = preset["quality"]
                self.quality_text.value = f"{preset['quality']}%"
            
            # 更新最大宽度
            if "max_width" in preset:
                self.max_width_field.value = str(preset["max_width"])
            else:
                self.max_width_field.value = ""
            
            # 更新最大高度
            if "max_height" in preset:
                self.max_height_field.value = str(preset["max_height"])
            else:
                self.max_height_field.value = ""
            
            self.page.update()
            
    def _on_quality_changed(self, e):
        """Handle quality slider change."""
        quality = int(e.control.value)
        self.quality_text.value = f"{quality}%"
        self.page.update()
        
    def _start_compression(self, e):
        """Start compression."""
        if not self.input_path:
            self._show_error("请选择输入文件")
            return
            
        if not self.output_path:
            self._show_error("请选择输出路径")
            return
            
        # 获取参数
        params = self._get_params()
        
        # 更新状态
        self.status_text.value = "正在压缩..."
        self.status_text.color = ft.Colors.BLUE
        self.progress_bar.value = 0
        self.page.update()
        
        # 在后台线程中执行压缩
        threading.Thread(
            target=self._compress_image,
            args=(params,),
            daemon=True,
        ).start()
        
    def _get_params(self):
        """Get compression parameters."""
        return {
            "input_path": self.input_path,
            "output_path": self.output_path,
            "format": self.format_dropdown.value,
            "quality": int(self.quality_slider.value),
            "max_width": int(self.max_width_field.value) if self.max_width_field.value else None,
            "max_height": int(self.max_height_field.value) if self.max_height_field.value else None,
            "backend": self.backend_dropdown.value,
        }
        
    def _compress_image(self, params):
        """Compress image in background thread."""
        try:
            # 模拟压缩过程
            import time
            
            # 更新进度
            for i in range(101):
                time.sleep(0.05)  # 模拟处理时间
                self.progress_bar.value = i / 100
                self.status_text.value = f"正在压缩... {i}%"
                self.page.update()
            
            # 这里应该调用实际的图像处理后端
            # 示例：使用Pillow
            try:
                from PIL import Image
                
                # 打开图片
                img = Image.open(params["input_path"])
                
                # 调整大小
                if params["max_width"] or params["max_height"]:
                    width, height = img.size
                    ratio = 1
                    
                    if params["max_width"] and width > params["max_width"]:
                        ratio = params["max_width"] / width
                        
                    if params["max_height"] and height > params["max_height"]:
                        height_ratio = params["max_height"] / height
                        ratio = min(ratio, height_ratio)
                    
                    if ratio < 1:
                        new_size = (int(width * ratio), int(height * ratio))
                        img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # 保存图片
                save_kwargs = {}
                if params["format"] in ["webp", "jpg", "jpeg"]:
                    save_kwargs["quality"] = params["quality"]
                
                img.save(params["output_path"], **save_kwargs)
                
                # 获取文件大小
                input_size = os.path.getsize(params["input_path"])
                output_size = os.path.getsize(params["output_path"])
                reduction = (1 - output_size / input_size) * 100
                
                # 更新结果
                self.result_text.value = (
                    f"压缩完成！\n"
                    f"原始大小: {input_size / 1024:.1f} KB\n"
                    f"压缩后: {output_size / 1024:.1f} KB\n"
                    f"压缩率: {reduction:.1f}%"
                )
                self.result_text.color = ft.Colors.GREEN
                
            except ImportError:
                self.result_text.value = "错误: 未安装Pillow库"
                self.result_text.color = ft.Colors.RED
                
        except Exception as ex:
            self.result_text.value = f"错误: {str(ex)}"
            self.result_text.color = ft.Colors.RED
            
        finally:
            self.status_text.value = "完成"
            self.status_text.color = ft.Colors.GREEN
            self.progress_bar.value = 1.0
            self.page.update()
            
    def _reset_params(self, e):
        """Reset parameters."""
        self.preset_dropdown.value = "Custom"
        self.format_dropdown.value = "webp"
        self.quality_slider.value = 82
        self.quality_text.value = "82%"
        self.max_width_field.value = "1920"
        self.max_height_field.value = ""
        self.backend_dropdown.value = "auto"
        self.input_field.value = ""
        self.output_field.value = ""
        self.input_path = ""
        self.output_path = ""
        self.progress_bar.value = 0
        self.status_text.value = "等待开始..."
        self.status_text.color = ft.Colors.GREY_500
        self.result_text.value = ""
        self.page.update()
        
    def _preview_image(self, e):
        """Preview image."""
        if not self.input_path:
            self._show_error("请先选择输入文件")
            return
            
        # 显示图片预览对话框
        dialog = ft.AlertDialog(
            title=ft.Text("图片预览"),
            content=ft.Image(
                src=self.input_path,
                width=500,
                height=400,
                fit=ft.ImageFit.CONTAIN,
            ),
            actions=[
                ft.TextButton("关闭", on_click=lambda e: self.page.close(dialog)),
            ],
        )
        
        self.page.open(dialog)
        
    def _show_error(self, message):
        """Show error message."""
        dialog = ft.AlertDialog(
            title=ft.Text("错误"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("确定", on_click=lambda e: self.page.close(dialog)),
            ],
        )
        
        self.page.open(dialog)