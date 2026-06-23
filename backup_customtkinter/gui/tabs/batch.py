"""Batch directory processing tab."""
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, List
from gui.styles.theme import COLORS, FONTS, SIZES, SPACING
from gui.widgets.file_selector import FileSelector
from gui.widgets.progress_item import ProgressItem
from gui.locales import COMMON, BATCH
from gui.utils.validators import (
    validate_quality,
    validate_dimensions,
    validate_target_size,
    validate_jobs,
    validate_directory_path
)


class BatchTab(ctk.CTkFrame):
    """Tab for batch directory processing."""
    
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
        self.results: List[dict] = []
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create UI
        self._create_input_section()
        self._create_params_section()
        self._create_action_section()
        self._create_result_section()
        
    def _create_input_section(self):
        """Create directory input section."""
        input_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=SIZES["corner_radius"])
        input_frame.grid(row=0, column=0, sticky="ew", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            input_frame,
            text=COMMON["input_output_dirs"],
            font=FONTS["subheading"],
            text_color=COLORS["text"]
        )
        title.grid(row=0, column=0, sticky="w", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))
        
        # Input directory selector
        self.input_selector = FileSelector(
            input_frame,
            mode="directory",
            label_text=BATCH["input_dir"]
        )
        self.input_selector.grid(row=1, column=0, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        # Output directory selector
        self.output_selector = FileSelector(
            input_frame,
            mode="directory",
            label_text=BATCH["output_dir"]
        )
        self.output_selector.grid(row=2, column=0, sticky="ew", padx=SIZES["padding"], pady=(SIZES["padding_small"], SIZES["padding"]))
        
    def _create_params_section(self):
        """Create parameters configuration section."""
        params_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=SIZES["corner_radius"])
        params_frame.grid(row=1, column=0, sticky="nsew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        params_frame.grid_columnconfigure(0, weight=1)
        params_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            params_frame,
            text=COMMON["compression_params"],
            font=FONTS["subheading"],
            text_color=COLORS["text"]
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))
        
        current_row = 1
        
        # Preset selection
        preset_label = ctk.CTkLabel(params_frame, text=COMMON["preset"], font=FONTS["body"])
        preset_label.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        self.preset_var = ctk.StringVar(value=COMMON["custom"])
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
        format_label = ctk.CTkLabel(params_frame, text=COMMON["output_format"], font=FONTS["body"])
        format_label.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        self.format_var = ctk.StringVar(value="webp")
        format_menu = ctk.CTkOptionMenu(
            params_frame,
            variable=self.format_var,
            values=self.FORMATS
        )
        format_menu.grid(row=current_row, column=1, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1
        
        # Quality slider
        quality_label = ctk.CTkLabel(params_frame, text=COMMON["quality"], font=FONTS["body"])
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
        width_label = ctk.CTkLabel(params_frame, text=COMMON["max_width"], font=FONTS["body"])
        width_label.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        self.max_width_var = ctk.StringVar(value="")
        width_entry = ctk.CTkEntry(
            params_frame,
            textvariable=self.max_width_var,
            placeholder_text=COMMON["leave_empty"],
            height=SIZES["entry_height"]
        )
        width_entry.grid(row=current_row, column=1, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1
        
        # Max height
        height_label = ctk.CTkLabel(params_frame, text=COMMON["max_height"], font=FONTS["body"])
        height_label.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        self.max_height_var = ctk.StringVar(value="")
        height_entry = ctk.CTkEntry(
            params_frame,
            textvariable=self.max_height_var,
            placeholder_text=COMMON["leave_empty"],
            height=SIZES["entry_height"]
        )
        height_entry.grid(row=current_row, column=1, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1
        
        # Target size
        target_label = ctk.CTkLabel(params_frame, text=COMMON["target_size"], font=FONTS["body"])
        target_label.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        self.target_size_var = ctk.StringVar(value="")
        target_entry = ctk.CTkEntry(
            params_frame,
            textvariable=self.target_size_var,
            placeholder_text=COMMON["target_hint"],
            height=SIZES["entry_height"]
        )
        target_entry.grid(row=current_row, column=1, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1
        
        # Backend selection
        backend_label = ctk.CTkLabel(params_frame, text=COMMON["backend"], font=FONTS["body"])
        backend_label.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        self.backend_var = ctk.StringVar(value="auto")
        backend_menu = ctk.CTkOptionMenu(
            params_frame,
            variable=self.backend_var,
            values=self.BACKENDS
        )
        backend_menu.grid(row=current_row, column=1, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1
        
        # Parallel jobs slider
        jobs_label = ctk.CTkLabel(params_frame, text=BATCH["parallel_jobs"], font=FONTS["body"])
        jobs_label.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        jobs_container = ctk.CTkFrame(params_frame, fg_color="transparent")
        jobs_container.grid(row=current_row, column=1, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        jobs_container.grid_columnconfigure(0, weight=1)
        
        self.jobs_var = ctk.IntVar(value=1)
        self.jobs_slider = ctk.CTkSlider(
            jobs_container,
            from_=1,
            to=16,
            variable=self.jobs_var,
            number_of_steps=15,
            progress_color=COLORS["primary"]
        )
        self.jobs_slider.grid(row=0, column=0, sticky="ew", padx=(0, SIZES["padding_small"]))
        
        self.jobs_label = ctk.CTkLabel(jobs_container, text="1", font=FONTS["body_bold"], width=40)
        self.jobs_label.grid(row=0, column=1)
        self.jobs_var.trace_add("write", lambda *args: self.jobs_label.configure(text=str(self.jobs_var.get())))
        current_row += 1
        
        # Strip metadata checkbox
        self.strip_meta_var = ctk.BooleanVar(value=True)
        strip_meta_check = ctk.CTkCheckBox(
            params_frame,
            text=COMMON["strip_metadata"],
            variable=self.strip_meta_var,
            font=FONTS["body"]
        )
        strip_meta_check.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1
        
        # Recursive checkbox
        self.recursive_var = ctk.BooleanVar(value=True)
        recursive_check = ctk.CTkCheckBox(
            params_frame,
            text=BATCH["recursive"],
            variable=self.recursive_var,
            font=FONTS["body"]
        )
        recursive_check.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1
        
        # Allow large images checkbox
        self.allow_large_var = ctk.BooleanVar(value=False)
        allow_large_check = ctk.CTkCheckBox(
            params_frame,
            text=COMMON["allow_large"],
            variable=self.allow_large_var,
            font=FONTS["body"]
        )
        allow_large_check.grid(row=current_row, column=0, columnspan=2, sticky="w", padx=SIZES["padding"], pady=(SIZES["padding_small"], SIZES["padding"]))
        
    def _create_action_section(self):
        """Create action buttons section."""
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=2, column=0, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        # Start button
        self.start_button = ctk.CTkButton(
            action_frame,
            text=BATCH["start_batch"],
            height=SIZES["button_height"] + 10,
            command=self._start_batch,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            font=FONTS["button"]
        )
        self.start_button.pack(side="left", padx=(0, SIZES["padding_small"]))
        
        # Clear button
        clear_button = ctk.CTkButton(
            action_frame,
            text=COMMON["clear"],
            height=SIZES["button_height"] + 10,
            command=self._clear_form,
            fg_color=COLORS["text_muted"],
            hover_color=COLORS["border"]
        )
        clear_button.pack(side="left")
        
    def _create_result_section(self):
        """Create result display section."""
        self.result_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=SIZES["corner_radius"])
        self.result_frame.grid(row=3, column=0, sticky="ew", padx=SIZES["padding"], pady=(SIZES["padding_small"], SIZES["padding"]))
        
        # Title with stats
        title_frame = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))
        
        title = ctk.CTkLabel(
            title_frame,
            text=COMMON["result"],
            font=FONTS["subheading"],
            text_color=COLORS["text"]
        )
        title.pack(side="left")
        
        self.stats_label = ctk.CTkLabel(
            title_frame,
            text="",
            font=FONTS["body"],
            text_color=COLORS["text_muted"]
        )
        self.stats_label.pack(side="right")
        
        # Progress and results container
        self.result_container = ctk.CTkScrollableFrame(
            self.result_frame,
            fg_color="transparent",
            height=200
        )
        self.result_container.pack(fill="both", expand=True, padx=SIZES["padding"], pady=(0, SIZES["padding"]))
        
    def _on_preset_changed(self, preset_name: str):
        """Handle preset selection change."""
        if preset_name == "Custom":
            return
            
        preset = self.PRESETS[preset_name]
        if preset:
            self.format_var.set(preset.get("format", "webp"))
            self.quality_var.set(preset.get("quality", 82))
            self.max_width_var.set(str(preset["max_width"]) if "max_width" in preset else "")
            self.max_height_var.set(str(preset["max_height"]) if "max_height" in preset else "")
            
    def _validate_params(self) -> tuple[bool, Optional[str]]:
        """Validate all parameters."""
        # Validate input directory
        input_dir = self.input_selector.get()
        is_valid, error = validate_directory_path(input_dir, must_exist=True)
        if not is_valid:
            return False, error
            
        # Validate output directory (can be non-existent, will be created)
        output_dir = self.output_selector.get()
        if not output_dir:
            return False, BATCH["output_dir_required"]
            
        # Validate quality
        is_valid, error = validate_quality(self.quality_var.get())
        if not is_valid:
            return False, error
            
        # Validate dimensions
        max_width = None
        max_height = None
        
        if self.max_width_var.get():
            try:
                max_width = int(self.max_width_var.get())
            except ValueError:
                return False, "最大宽度必须是有效的整数"
                
        if self.max_height_var.get():
            try:
                max_height = int(self.max_height_var.get())
            except ValueError:
                return False, "最大高度必须是有效的整数"
                
        is_valid, error = validate_dimensions(max_width, max_height, self.format_var.get())
        if not is_valid:
            return False, error
            
        # Validate target size
        if self.target_size_var.get():
            try:
                target_size = int(self.target_size_var.get())
                is_valid, error = validate_target_size(target_size)
                if not is_valid:
                    return False, error
            except ValueError:
                return False, "目标大小必须是有效的整数"
                
        # Validate jobs
        is_valid, error = validate_jobs(self.jobs_var.get())
        if not is_valid:
            return False, error
            
        return True, None
        
    def _start_batch(self):
        """Start the batch processing."""
        # Validate parameters
        is_valid, error = self._validate_params()
        if not is_valid:
            messagebox.showerror(BATCH["validation_error"], error)
            return
            
        # Collect parameters
        params = self._collect_params()
        
        # Update UI
        self.start_button.configure(state="disabled", text=BATCH["processing"])
        self.app.update_status(BATCH["batch_processing"])
        
        # Clear previous results
        for widget in self.result_container.winfo_children():
            widget.destroy()
        self.results = []
        self.stats_label.configure(text="")
        
        # Create progress item
        self.current_task = ProgressItem(
            self.result_container,
            task_name=f"{BATCH['batch_task']}: {params['source_dir']}",
            show_cancel=False
        )
        self.current_task.pack(fill="x", pady=SIZES["padding_small"])
        self.current_task.set_status("processing", "正在处理...")
        
        # Run batch processing in background
        self._run_batch(params)
        
    def _collect_params(self) -> dict:
        """Collect all parameters into a dictionary."""
        params = {
            "source_dir": self.input_selector.get(),
            "out": self.output_selector.get(),
            "format": self.format_var.get(),
            "quality": self.quality_var.get(),
            "strip_meta": self.strip_meta_var.get(),
            "recursive": self.recursive_var.get(),
            "backend": self.backend_var.get(),
            "allow_large": self.allow_large_var.get(),
            "jobs": self.jobs_var.get(),
        }
        
        if self.max_width_var.get():
            params["max_width"] = int(self.max_width_var.get())
        if self.max_height_var.get():
            params["max_height"] = int(self.max_height_var.get())
        if self.target_size_var.get():
            params["target_size"] = int(self.target_size_var.get())
            
        return params
        
    def _run_batch(self, params: dict):
        """Run batch processing (placeholder - will be implemented with threading)."""
        import threading
        
        def worker():
            try:
                # Import PicX
                from picx import optimize_dir
                
                # Run optimization
                results = optimize_dir(**params)
                
                # Update UI on success
                self.after(0, lambda: self._on_batch_complete(results))
            except Exception as e:
                # Update UI on error
                self.after(0, lambda: self._on_batch_error(str(e)))
                
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        
    def _on_batch_complete(self, results):
        """Handle successful batch processing."""
        self.start_button.configure(state="normal", text=BATCH["start_batch"])
        self.app.update_status("批量处理完成")
        
        self.results = results
        
        if self.current_task:
            # Count successes and errors
            successes = sum(1 for r in results if not r.error)
            errors = len(results) - successes
            
            if errors == 0:
                self.current_task.set_status("success", f"完成: {successes} 个文件")
            else:
                self.current_task.set_status("error", f"完成: {successes}, 失败: {errors}")
                
        # Update stats
        total_original = sum(r.original_size for r in results if not r.error)
        total_output = sum(r.output_size for r in results if not r.error)
        savings = ((total_original - total_output) / total_original * 100) if total_original > 0 else 0
        
        self.stats_label.configure(
            text=f"总计: {len(results)} 个文件 | 节省: {savings:.1f}%"
        )
        
        # Show results in list (limited to first 10)
        for i, result in enumerate(results[:10]):
            if not result.error:
                self._add_result_item(
                    result.source_path,
                    result.original_size,
                    result.output_size,
                    "success"
                )
            else:
                self._add_result_item(
                    result.source_path,
                    0,
                    0,
                    "error",
                    str(result.error)
                )
                
        if len(results) > 10:
            more_label = ctk.CTkLabel(
                self.result_container,
                text=f"... 还有 {len(results) - 10} 个文件",
                font=FONTS["small"],
                text_color=COLORS["text_muted"]
            )
            more_label.pack(pady=SIZES["padding_small"])
            
    def _add_result_item(self, filename: str, original_size: int, output_size: int, status: str, error_msg: str = ""):
        """Add a result item to the list."""
        item_frame = ctk.CTkFrame(self.result_container, fg_color=COLORS["surface_light"], corner_radius=4)
        item_frame.pack(fill="x", pady=2)
        
        # Status icon
        status_icon = "✓" if status == "success" else "✗"
        icon_color = COLORS["success"] if status == "success" else COLORS["error"]
        
        icon_label = ctk.CTkLabel(
            item_frame,
            text=status_icon,
            text_color=icon_color,
            font=FONTS["body_bold"],
            width=30
        )
        icon_label.pack(side="left", padx=(10, 5), pady=5)
        
        # Filename
        name_label = ctk.CTkLabel(
            item_frame,
            text=filename,
            font=FONTS["body"],
            text_color=COLORS["text"],
            anchor="w"
        )
        name_label.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # Size info
        if status == "success" and original_size > 0:
            original_mb = original_size / (1024 * 1024)
            output_mb = output_size / (1024 * 1024)
            savings = ((original_size - output_size) / original_size * 100) if original_size > 0 else 0
            
            size_text = f"{original_mb:.2f}MB → {output_mb:.2f}MB ({savings:.1f}%)"
        else:
            size_text = error_msg if error_msg else "处理失败"
            
        size_label = ctk.CTkLabel(
            item_frame,
            text=size_text,
            font=FONTS["small"],
            text_color=COLORS["text_muted"],
            anchor="e"
        )
        size_label.pack(side="right", padx=(5, 10), pady=5)
        
    def _on_batch_error(self, error_msg: str):
        """Handle batch processing error."""
        self.start_button.configure(state="normal", text=BATCH["start_batch"])
        self.app.update_status("批量处理失败")
        
        if self.current_task:
            self.current_task.set_status("error", f"错误: {error_msg}")
            
        messagebox.showerror(BATCH["failed"], f"批量处理时发生错误:\n{error_msg}")
        
    def _clear_form(self):
        """Clear the form."""
        self.input_selector.clear()
        self.output_selector.clear()
        self.preset_var.set("Custom")
        self.format_var.set("webp")
        self.quality_var.set(82)
        self.max_width_var.set("")
        self.max_height_var.set("")
        self.target_size_var.set("")
        self.backend_var.set("auto")
        self.jobs_var.set(1)
        self.strip_meta_var.set(True)
        self.recursive_var.set(True)
        self.allow_large_var.set(False)
        
        # Clear results
        for widget in self.result_container.winfo_children():
            widget.destroy()
        self.results = []
        self.stats_label.configure(text="")
