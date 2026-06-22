"""Optimized single image compression tab with improved UI layout."""
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional
from gui.styles.theme import COLORS, FONTS, SIZES
from gui.widgets.file_selector import FileSelector
from gui.widgets.progress_item import ProgressItem


class SingleImageTabOptimized(ctk.CTkFrame):
    """Optimized tab for single image compression with better layout."""

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

    def __init__(self, master, app_instance, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.app = app_instance
        self.current_task = None

        # Configure grid - use scrollable frame for better layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create scrollable container
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # Create UI sections
        self._create_input_section()
        self._create_params_section()
        self._create_action_section()
        self._create_result_section()

    def _create_input_section(self):
        """Create file input section."""
        input_frame = ctk.CTkFrame(self.scroll_frame, fg_color=COLORS["surface"], corner_radius=SIZES["corner_radius"])
        input_frame.grid(row=0, column=0, sticky="ew", padx=SIZES["padding"], pady=(0, SIZES["padding_small"]))
        input_frame.grid_columnconfigure(0, weight=1)

        # Title
        title = ctk.CTkLabel(
            input_frame,
            text="输入与输出",
            font=FONTS["subheading"],
            text_color=COLORS["text"]
        )
        title.grid(row=0, column=0, sticky="w", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))

        # Input file selector
        self.input_selector = FileSelector(
            input_frame,
            mode="file",
            label_text="输入图片:",
            filetypes=[
                ("图片文件", "*.png *.jpg *.jpeg *.webp *.avif *.tif *.tiff"),
                ("所有文件", "*.*")
            ]
        )
        self.input_selector.grid(row=1, column=0, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])

        # Output file selector
        self.output_selector = FileSelector(
            input_frame,
            mode="save",
            label_text="输出路径:",
            filetypes=[
                ("WebP", "*.webp"),
                ("JPEG", "*.jpg"),
                ("PNG", "*.png"),
                ("AVIF", "*.avif"),
                ("TIFF", "*.tiff"),
            ]
        )
        self.output_selector.grid(row=2, column=0, sticky="ew", padx=SIZES["padding"], pady=(SIZES["padding_small"], SIZES["padding"]))

    def _create_params_section(self):
        """Create parameters configuration section."""
        params_frame = ctk.CTkFrame(self.scroll_frame, fg_color=COLORS["surface"], corner_radius=SIZES["corner_radius"])
        params_frame.grid(row=1, column=0, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        params_frame.grid_columnconfigure(0, weight=1)
        params_frame.grid_columnconfigure(1, weight=1)

        # Title
        title = ctk.CTkLabel(
            params_frame,
            text="压缩参数",
            font=FONTS["subheading"],
            text_color=COLORS["text"]
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))

        current_row = 1

        # Preset selection
        preset_label = ctk.CTkLabel(params_frame, text="预设:", font=FONTS["body"])
        preset_label.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])

        self.preset_var = ctk.StringVar(value="Custom")
        preset_menu = ctk.CTkOptionMenu(
            params_frame,
            variable=self.preset_var,
            values=list(self.PRESETS.keys()),
            command=self._on_preset_changed,
            fg_color=COLORS["primary"],
            button_color=COLORS["primary_hover"]
        )
        preset_menu.grid(row=current_row, column=1, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1

        # Output format
        format_label = ctk.CTkLabel(params_frame, text="输出格式:", font=FONTS["body"])
        format_label.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])

        self.format_var = ctk.StringVar(value="webp")
        format_menu = ctk.CTkOptionMenu(
            params_frame,
            variable=self.format_var,
            values=self.FORMATS,
            command=self._on_format_changed
        )
        format_menu.grid(row=current_row, column=1, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1

        # Quality slider
        quality_label = ctk.CTkLabel(params_frame, text="质量:", font=FONTS["body"])
        quality_label.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])

        quality_container = ctk.CTkFrame(params_frame, fg_color="transparent")
        quality_container.grid(row=current_row, column=1, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        quality_container.grid_columnconfigure(0, weight=1)

        self.quality_var = ctk.IntVar(value=82)
        self.quality_slider = ctk.CTkSlider(
            quality_container,
            from_=1,
            to=100,
            variable=self.quality_var,
            number_of_steps=99,
            progress_color=COLORS["primary"]
        )
        self.quality_slider.grid(row=0, column=0, sticky="ew", padx=(0, SIZES["padding_small"]))

        self.quality_label = ctk.CTkLabel(quality_container, text="82", font=FONTS["body_bold"], width=40)
        self.quality_label.grid(row=0, column=1)
        self.quality_var.trace_add("write", lambda *args: self.quality_label.configure(text=str(self.quality_var.get())))
        current_row += 1

        # Max width
        width_label = ctk.CTkLabel(params_frame, text="最大宽度 (px):", font=FONTS["body"])
        width_label.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])

        self.max_width_var = ctk.StringVar(value="")
        width_entry = ctk.CTkEntry(
            params_frame,
            textvariable=self.max_width_var,
            placeholder_text="留空保持原始尺寸",
            height=SIZES["entry_height"]
        )
        width_entry.grid(row=current_row, column=1, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1

        # Max height
        height_label = ctk.CTkLabel(params_frame, text="最大高度 (px):", font=FONTS["body"])
        height_label.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])

        self.max_height_var = ctk.StringVar(value="")
        height_entry = ctk.CTkEntry(
            params_frame,
            textvariable=self.max_height_var,
            placeholder_text="留空保持原始尺寸",
            height=SIZES["entry_height"]
        )
        height_entry.grid(row=current_row, column=1, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1

        # Target size
        target_label = ctk.CTkLabel(params_frame, text="目标大小 (字节):", font=FONTS["body"])
        target_label.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])

        self.target_size_var = ctk.StringVar(value="")
        target_entry = ctk.CTkEntry(
            params_frame,
            textvariable=self.target_size_var,
            placeholder_text="例如: 120000 约等于 120KB",
            height=SIZES["entry_height"]
        )
        target_entry.grid(row=current_row, column=1, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1

        # Backend selection
        backend_label = ctk.CTkLabel(params_frame, text="后端:", font=FONTS["body"])
        backend_label.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])

        self.backend_var = ctk.StringVar(value="auto")
        backend_menu = ctk.CTkOptionMenu(
            params_frame,
            variable=self.backend_var,
            values=self.BACKENDS
        )
        backend_menu.grid(row=current_row, column=1, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1

        # Strip metadata checkbox
        self.strip_meta_var = ctk.BooleanVar(value=True)
        strip_meta_check = ctk.CTkCheckBox(
            params_frame,
            text="去除元数据",
            variable=self.strip_meta_var,
            font=FONTS["body"]
        )
        strip_meta_check.grid(row=current_row, column=0, columnspan=2, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1

        # Allow large images checkbox
        self.allow_large_var = ctk.BooleanVar(value=False)
        allow_large_check = ctk.CTkCheckBox(
            params_frame,
            text="允许大图 (仅限可信来源)",
            variable=self.allow_large_var,
            font=FONTS["body"]
        )
        allow_large_check.grid(row=current_row, column=0, columnspan=2, sticky="w", padx=SIZES["padding"], pady=(SIZES["padding_small"], SIZES["padding"]))

    def _create_action_section(self):
        """Create action buttons section."""
        action_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        action_frame.grid(row=2, column=0, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])

        # Start button
        self.start_button = ctk.CTkButton(
            action_frame,
            text="开始压缩",
            height=SIZES["button_height"] + 10,
            command=self._start_compression,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            font=FONTS["button"]
        )
        self.start_button.pack(side="left", padx=(0, SIZES["padding_small"]))

        # Clear button
        clear_button = ctk.CTkButton(
            action_frame,
            text="清空",
            height=SIZES["button_height"] + 10,
            command=self._clear_form,
            fg_color=COLORS["text_muted"],
            hover_color=COLORS["border"]
        )
        clear_button.pack(side="left")

    def _create_result_section(self):
        """Create result display section."""
        self.result_frame = ctk.CTkFrame(self.scroll_frame, fg_color=COLORS["surface"], corner_radius=SIZES["corner_radius"])
        self.result_frame.grid(row=3, column=0, sticky="ew", padx=SIZES["padding"], pady=(SIZES["padding_small"], 0))

        # Title
        title = ctk.CTkLabel(
            self.result_frame,
            text="结果",
            font=FONTS["subheading"],
            text_color=COLORS["text"]
        )
        title.pack(anchor="w", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))

        # Result will be added here dynamically
        self.result_container = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        self.result_container.pack(fill="both", expand=True, padx=SIZES["padding"], pady=(0, SIZES["padding"]))

    def _on_preset_changed(self, choice):
        """Handle preset selection change."""
        preset = self.PRESETS.get(choice)
        if preset:
            self.format_var.set(preset.get("format", "webp"))
            self.quality_var.set(preset.get("quality", 82))
            self.max_width_var.set(str(preset.get("max_width", "")) if "max_width" in preset else "")
            self.max_height_var.set(str(preset.get("max_height", "")) if "max_height" in preset else "")

    def _on_format_changed(self, choice):
        """Handle format change."""
        if choice == "png" and self.quality_var.get() < 100:
            self.quality_var.set(100)

    def _start_compression(self):
        """Start compression process."""
        # Validate inputs
        input_path = self.input_selector.get_path()
        if not input_path:
            messagebox.showerror("错误", "请选择输入图片")
            return

        output_path = self.output_selector.get_path()
        if not output_path:
            messagebox.showerror("错误", "请选择输出路径")
            return

        # Get parameters
        params = {
            "format": self.format_var.get(),
            "quality": self.quality_var.get(),
            "max_width": self.max_width_var.get() or None,
            "max_height": self.max_height_var.get() or None,
            "target_size": self.target_size_var.get() or None,
            "backend": self.backend_var.get(),
            "strip_metadata": self.strip_meta_var.get(),
            "allow_large": self.allow_large_var.get(),
        }

        # Clear previous results
        for widget in self.result_container.winfo_children():
            widget.destroy()

        # Create progress item
        progress = ProgressItem(self.result_container)
        progress.pack(fill="x", pady=2)
        progress.set_status("processing", "处理中...")

        # Disable start button
        self.start_button.configure(state="disabled")

        # Run compression in background
        import threading
        thread = threading.Thread(
            target=self._run_compression,
            args=(input_path, output_path, params, progress),
            daemon=True
        )
        thread.start()

    def _run_compression(self, input_path, output_path, params, progress):
        """Run compression in background thread."""
        try:
            from picx import compress_image

            result = compress_image(
                input_path=input_path,
                output_path=output_path,
                **params
            )

            # Update UI in main thread
            self.after(0, lambda: self._on_compression_complete(result, progress))

        except Exception as e:
            self.after(0, lambda: self._on_compression_error(str(e), progress))

    def _on_compression_complete(self, result, progress):
        """Handle compression completion."""
        self.start_button.configure(state="normal")

        if result.get("success"):
            original_size = result.get("original_size", 0)
            compressed_size = result.get("compressed_size", 0)
            ratio = result.get("compression_ratio", 0)

            size_str = f"{original_size:,} -> {compressed_size:,} bytes"
            ratio_str = f"压缩率: {ratio:.1f}%"

            progress.set_status("success", f"完成 - {ratio_str}")

            # Show details
            details = ctk.CTkLabel(
                self.result_container,
                text=f"{size_str}\n{ratio_str}",
                font=FONTS["body"],
                text_color=COLORS["text"]
            )
            details.pack(anchor="w", padx=10, pady=5)
        else:
            error = result.get("error", "未知错误")
            progress.set_status("error", f"失败: {error}")

    def _on_compression_error(self, error, progress):
        """Handle compression error."""
        self.start_button.configure(state="normal")
        progress.set_status("error", f"错误: {error}")

    def _clear_form(self):
        """Clear form and results."""
        self.input_selector.clear()
        self.output_selector.clear()
        self.format_var.set("webp")
        self.quality_var.set(82)
        self.max_width_var.set("")
        self.max_height_var.set("")
        self.target_size_var.set("")
        self.backend_var.set("auto")
        self.strip_meta_var.set(True)
        self.allow_large_var.set(False)
        self.preset_var.set("Custom")

        # Clear results
        for widget in self.result_container.winfo_children():
            widget.destroy()
