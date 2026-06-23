"""Batch processing tab."""
import flet as ft
import os
import threading
from typing import List, Dict, Any


class BatchTab:
    """Tab for batch image processing."""
    
    # PicX presets
    PRESETS = {
        "Custom": None,
        "web": {"format": "webp", "quality": 82, "max_width": 1920},
        "blog": {"format": "webp", "quality": 78, "max_width": 1600},
        "avatar": {"format": "webp", "quality": 85, "max_width": 256, "max_height": 256},
        "lossless": {"format": "png", "quality": 100},
    }
    
    FORMATS = ["保持原格式", "webp", "jpg", "png", "avif", "tiff"]
    BACKENDS = ["auto", "pillow", "pyvips"]
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.source_dir = ""
        self.output_dir = ""
        self.files: List[str] = []
        self.is_processing = False
        self.stop_processing = False
        
        # UI components
        self.source_field = None
        self.output_field = None
        self.file_list_text = None
        self.file_count_text = None
        self.preset_dropdown = None
        self.format_dropdown = None
        self.quality_slider = None
        self.quality_text = None
        self.max_width_field = None
        self.max_height_field = None
        self.backend_dropdown = None
        self.overwrite_checkbox = None
        self.keep_structure_checkbox = None
        self.progress_bar = None
        self.status_text = None
        self.result_text = None
        
    def build(self):
        """Build the tab content."""
        return ft.Container(
            content=ft.Column([
                # 输入目录选择
                self._create_input_section(),
                # 批量处理参数
                self._create_params_section(),
                # 文件列表
                self._create_file_list_section(),
                # 操作按钮
                self._create_action_section(),
                # 进度和结果
                self._create_progress_section(),
            ], spacing=15, scroll=ft.ScrollMode.AUTO),
            padding=20,
        )
        
    def _create_input_section(self):
        """Create input section."""
        # 源目录选择
        self.source_field = ft.TextField(
            label="源目录",
            hint_text="选择图片目录",
            expand=True,
            read_only=True,
        )
        
        # 输出目录选择
        self.output_field = ft.TextField(
            label="输出目录",
            hint_text="选择保存目录",
            expand=True,
            read_only=True,
        )
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("输入目录", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Row([
                        self.source_field,
                        ft.ElevatedButton(
                            "浏览...",
                            icon=ft.Icons.FOLDER_OPEN,
                            on_click=self._select_source_dir,
                        ),
                    ]),
                    ft.Row([
                        self.output_field,
                        ft.ElevatedButton(
                            "浏览...",
                            icon=ft.Icons.FOLDER_OPEN,
                            on_click=self._select_output_dir,
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
            width=150,
            options=[ft.dropdown.Option(fmt) for fmt in self.FORMATS],
            value="保持原格式",
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
        
        # 复选框
        self.overwrite_checkbox = ft.Checkbox(label="覆盖现有文件", value=False)
        self.keep_structure_checkbox = ft.Checkbox(label="保留目录结构", value=True)
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("批量处理参数", size=16, weight=ft.FontWeight.BOLD),
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
                    # 复选框
                    ft.Row([
                        self.overwrite_checkbox,
                        self.keep_structure_checkbox,
                    ]),
                ], spacing=10),
                padding=20,
            )
        )
        
    def _create_file_list_section(self):
        """Create file list section."""
        self.file_count_text = ft.Text("0 个文件", color=ft.Colors.GREY_500)
        self.file_list_text = ft.Text("请先选择源目录", color=ft.Colors.GREY_500)
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("文件列表", size=16, weight=ft.FontWeight.BOLD),
                        self.file_count_text,
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(),
                    ft.Container(
                        content=ft.Column([self.file_list_text], spacing=5),
                        height=200,
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=10,
                        padding=10,
                    ),
                ], spacing=10),
                padding=20,
            )
        )
        
    def _create_action_section(self):
        """Create action section."""
        return ft.Row([
            ft.ElevatedButton(
                "开始批量处理",
                icon=ft.Icons.PLAY_ARROW,
                on_click=self._start_batch,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.AMBER,
                    color=ft.Colors.WHITE,
                ),
            ),
            ft.OutlinedButton(
                "停止",
                icon=ft.Icons.STOP,
                on_click=self._stop_batch,
            ),
            ft.OutlinedButton(
                "扫描文件",
                icon=ft.Icons.REFRESH,
                on_click=self._scan_files,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER)
        
    def _create_progress_section(self):
        """Create progress section."""
        self.progress_bar = ft.ProgressBar(value=0, color=ft.Colors.AMBER)
        self.status_text = ft.Text("等待开始...", color=ft.Colors.GREY_500)
        self.result_text = ft.Text("")
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("处理进度", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    self.progress_bar,
                    self.status_text,
                    self.result_text,
                ], spacing=10),
                padding=20,
            )
        )
        
    def _select_source_dir(self, e):
        """Handle source directory selection."""
        file_picker = ft.FilePicker(
            on_result=self._on_source_dir_picked,
        )
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.get_directory_path()
        
    def _on_source_dir_picked(self, e):
        """Handle source directory picked."""
        if e.path:
            self.source_dir = e.path
            self.source_field.value = self.source_dir
            self.page.update()
            self._scan_files(None)
            
    def _select_output_dir(self, e):
        """Handle output directory selection."""
        file_picker = ft.FilePicker(
            on_result=self._on_output_dir_picked,
        )
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.get_directory_path()
        
    def _on_output_dir_picked(self, e):
        """Handle output directory picked."""
        if e.path:
            self.output_dir = e.path
            self.output_field.value = self.output_dir
            self.page.update()
            
    def _scan_files(self, e):
        """Scan files in source directory."""
        if not self.source_dir:
            self._show_error("请先选择源目录")
            return
            
        # 支持的图片格式
        image_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.avif', '.tif', '.tiff'}
        
        # 扫描文件
        self.files = []
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                if os.path.splitext(file)[1].lower() in image_extensions:
                    self.files.append(os.path.join(root, file))
        
        # 更新UI
        self.file_count_text.value = f"{len(self.files)} 个文件"
        if self.files:
            # 显示前10个文件
            display_files = self.files[:10]
            file_list = "\n".join([os.path.basename(f) for f in display_files])
            if len(self.files) > 10:
                file_list += f"\n... 还有 {len(self.files) - 10} 个文件"
            self.file_list_text.value = file_list
            self.file_list_text.color = ft.Colors.GREY_700
        else:
            self.file_list_text.value = "未找到图片文件"
            self.file_list_text.color = ft.Colors.GREY_500
            
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
        
    def _start_batch(self, e):
        """Start batch processing."""
        if not self.source_dir:
            self._show_error("请选择源目录")
            return
            
        if not self.output_dir:
            self._show_error("请选择输出目录")
            return
            
        if not self.files:
            self._show_error("没有找到图片文件")
            return
            
        # 获取参数
        params = self._get_params()
        
        # 更新状态
        self.is_processing = True
        self.stop_processing = False
        self.status_text.value = "正在处理..."
        self.status_text.color = ft.Colors.BLUE
        self.progress_bar.value = 0
        self.page.update()
        
        # 在后台线程中执行批量处理
        threading.Thread(
            target=self._process_batch,
            args=(params,),
            daemon=True,
        ).start()
        
    def _get_params(self):
        """Get processing parameters."""
        return {
            "source_dir": self.source_dir,
            "output_dir": self.output_dir,
            "format": self.format_dropdown.value,
            "quality": int(self.quality_slider.value),
            "max_width": int(self.max_width_field.value) if self.max_width_field.value else None,
            "max_height": int(self.max_height_field.value) if self.max_height_field.value else None,
            "backend": self.backend_dropdown.value,
            "overwrite": self.overwrite_checkbox.value,
            "keep_structure": self.keep_structure_checkbox.value,
        }
        
    def _process_batch(self, params):
        """Process batch in background thread."""
        try:
            total_files = len(self.files)
            processed_files = 0
            success_files = 0
            error_files = 0
            
            for i, file_path in enumerate(self.files):
                if self.stop_processing:
                    break
                    
                try:
                    # 计算输出路径
                    if params["keep_structure"]:
                        # 保持目录结构
                        rel_path = os.path.relpath(file_path, params["source_dir"])
                        output_path = os.path.join(params["output_dir"], rel_path)
                    else:
                        # 扁平结构
                        output_path = os.path.join(params["output_dir"], os.path.basename(file_path))
                    
                    # 修改扩展名
                    if params["format"] != "保持原格式":
                        output_path = os.path.splitext(output_path)[0] + f".{params['format']}"
                    
                    # 创建输出目录
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    
                    # 检查是否覆盖
                    if os.path.exists(output_path) and not params["overwrite"]:
                        continue
                    
                    # 这里应该调用实际的图像处理后端
                    # 示例：使用Pillow
                    try:
                        from PIL import Image
                        
                        # 打开图片
                        img = Image.open(file_path)
                        
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
                        
                        img.save(output_path, **save_kwargs)
                        success_files += 1
                        
                    except ImportError:
                        error_files += 1
                        
                except Exception as ex:
                    error_files += 1
                    
                finally:
                    processed_files += 1
                    
                    # 更新进度
                    progress = processed_files / total_files
                    self.progress_bar.value = progress
                    self.status_text.value = f"正在处理... {processed_files}/{total_files}"
                    self.page.update()
            
            # 更新结果
            self.result_text.value = (
                f"批量处理完成！\n"
                f"总文件数: {total_files}\n"
                f"成功: {success_files}\n"
                f"失败: {error_files}"
            )
            self.result_text.color = ft.Colors.GREEN
            
        except Exception as ex:
            self.result_text.value = f"错误: {str(ex)}"
            self.result_text.color = ft.Colors.RED
            
        finally:
            self.is_processing = False
            self.status_text.value = "完成"
            self.status_text.color = ft.Colors.GREEN
            self.progress_bar.value = 1.0
            self.page.update()
            
    def _stop_batch(self, e):
        """Stop batch processing."""
        self.stop_processing = True
        self.status_text.value = "正在停止..."
        self.status_text.color = ft.Colors.ORANGE
        self.page.update()
        
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