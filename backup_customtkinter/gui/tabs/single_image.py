"""Single image compression tab."""
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional
from gui.styles.theme import COLORS, FONTS, SIZES
from gui.widgets.file_selector import FileSelector
from gui.widgets.progress_item import ProgressItem
from gui.utils.validators import (
    validate_quality,
    validate_dimensions,
    validate_target_size,
    validate_file_path
)


class SingleImageTab(ctk.CTkFrame):
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
    
    def __init__(self, master, app_instance, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.app = app_instance
        self.current_task = None
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create UI
        self._create_input_section()
        self._create_params_section()
        self._create_action_section()
        self._create_result_section()
        
    def _create_input_section(self):
        """Create file input section."""
        input_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=SIZES["corner_radius"])
        input_frame.grid(row=0, column=0, sticky="ew", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            input_frame,
            text="Input & Output",
            font=FONTS["subheading"],
            text_color=COLORS["text"]
        )
        title.grid(row=0, column=0, sticky="w", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))
        
        # Input file selector
        self.input_selector = FileSelector(
            input_frame,
            mode="file",
            label_text="Input Image:",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.webp *.avif *.tif *.tiff"),
                ("All files", "*.*")
            ]
        )
        self.input_selector.grid(row=1, column=0, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        # Output file selector
        self.output_selector = FileSelector(
            input_frame,
            mode="save",
            label_text="Output Path:",
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
        params_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=SIZES["corner_radius"])
        params_frame.grid(row=1, column=0, sticky="nsew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        params_frame.grid_columnconfigure(0, weight=1)
        params_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            params_frame,
            text="Compression Parameters",
            font=FONTS["subheading"],
            text_color=COLORS["text"]
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))
        
        current_row = 1
        
        # Preset selection
        preset_label = ctk.CTkLabel(params_frame, text="Preset:", font=FONTS["body"])
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
        format_label = ctk.CTkLabel(params_frame, text="Output Format:", font=FONTS["body"])
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
        quality_label = ctk.CTkLabel(params_frame, text="Quality:", font=FONTS["body"])
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
        width_label = ctk.CTkLabel(params_frame, text="Max Width (px):", font=FONTS["body"])
        width_label.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        self.max_width_var = ctk.StringVar(value="")
        width_entry = ctk.CTkEntry(
            params_frame,
            textvariable=self.max_width_var,
            placeholder_text="Leave empty for original",
            height=SIZES["entry_height"]
        )
        width_entry.grid(row=current_row, column=1, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1
        
        # Max height
        height_label = ctk.CTkLabel(params_frame, text="Max Height (px):", font=FONTS["body"])
        height_label.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        self.max_height_var = ctk.StringVar(value="")
        height_entry = ctk.CTkEntry(
            params_frame,
            textvariable=self.max_height_var,
            placeholder_text="Leave empty for original",
            height=SIZES["entry_height"]
        )
        height_entry.grid(row=current_row, column=1, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1
        
        # Target size
        target_label = ctk.CTkLabel(params_frame, text="Target Size (bytes):", font=FONTS["body"])
        target_label.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        self.target_size_var = ctk.StringVar(value="")
        target_entry = ctk.CTkEntry(
            params_frame,
            textvariable=self.target_size_var,
            placeholder_text="e.g., 120000 for ~120KB",
            height=SIZES["entry_height"]
        )
        target_entry.grid(row=current_row, column=1, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1
        
        # Backend selection
        backend_label = ctk.CTkLabel(params_frame, text="Backend:", font=FONTS["body"])
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
            text="Strip metadata",
            variable=self.strip_meta_var,
            font=FONTS["body"]
        )
        strip_meta_check.grid(row=current_row, column=0, columnspan=2, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1
        
        # Allow large images checkbox
        self.allow_large_var = ctk.BooleanVar(value=False)
        allow_large_check = ctk.CTkCheckBox(
            params_frame,
            text="Allow large images (trusted sources only)",
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
            text="Start Compression",
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
            text="Clear",
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
        
        # Title
        title = ctk.CTkLabel(
            self.result_frame,
            text="Result",
            font=FONTS["subheading"],
            text_color=COLORS["text"]
        )
        title.pack(anchor="w", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))
        
        # Result will be added here dynamically
        self.result_container = ctk.CTkFrame(self.result_frame, fg_color="transparent")
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
            
    def _on_format_changed(self, format_name: str):
        """Handle format change."""
        # Validate dimensions for WebP
        if format_name == "webp":
            max_width = self.max_width_var.get()
            if max_width and int(max_width) > 16383:
                messagebox.showwarning(
                    "WebP Limitation",
                    "WebP format has a maximum dimension of 16383 pixels. Width will be capped."
                )
                
    def _validate_params(self) -> tuple[bool, Optional[str]]:
        """Validate all parameters."""
        # Validate input path
        input_path = self.input_selector.get()
        is_valid, error = validate_file_path(input_path, must_exist=True)
        if not is_valid:
            return False, error
            
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
                return False, "Max width must be a valid integer"
                
        if self.max_height_var.get():
            try:
                max_height = int(self.max_height_var.get())
            except ValueError:
                return False, "Max height must be a valid integer"
                
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
                return False, "Target size must be a valid integer"
                
        return True, None
        
    def _start_compression(self):
        """Start the compression process."""
        # Validate parameters
        is_valid, error = self._validate_params()
        if not is_valid:
            messagebox.showerror("Validation Error", error)
            return
            
        # Collect parameters
        params = self._collect_params()
        
        # Update UI
        self.start_button.configure(state="disabled", text="Processing...")
        self.app.update_status("Compressing image...")
        
        # Clear previous result
        for widget in self.result_container.winfo_children():
            widget.destroy()
            
        # Create progress item
        self.current_task = ProgressItem(
            self.result_container,
            task_name=f"Compressing {params['source']}",
            show_cancel=False
        )
        self.current_task.pack(fill="x", pady=SIZES["padding_small"])
        self.current_task.set_status("processing", "Starting compression...")
        
        # Run compression in background
        self._run_compression(params)
        
    def _collect_params(self) -> dict:
        """Collect all parameters into a dictionary."""
        params = {
            "source": self.input_selector.get(),
            "output": self.output_selector.get() or None,
            "format": self.format_var.get(),
            "quality": self.quality_var.get(),
            "strip_meta": self.strip_meta_var.get(),
            "backend": self.backend_var.get(),
            "allow_large": self.allow_large_var.get(),
        }
        
        if self.max_width_var.get():
            params["max_width"] = int(self.max_width_var.get())
        if self.max_height_var.get():
            params["max_height"] = int(self.max_height_var.get())
        if self.target_size_var.get():
            params["target_size"] = int(self.target_size_var.get())
            
        return params
        
    def _run_compression(self, params: dict):
        """Run compression (placeholder - will be implemented with threading)."""
        import threading
        
        def worker():
            try:
                # Import PicX
                from picx import optimize_image
                
                # Run optimization
                result = optimize_image(**params)
                
                # Update UI on success
                self.after(0, lambda: self._on_compression_complete(result))
            except Exception as e:
                # Update UI on error
                self.after(0, lambda: self._on_compression_error(str(e)))
                
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        
    def _on_compression_complete(self, result):
        """Handle successful compression."""
        self.start_button.configure(state="normal", text="Start Compression")
        self.app.update_status("Compression completed successfully")
        
        if self.current_task:
            # Format result message
            original_mb = result.original_size / (1024 * 1024)
            output_mb = result.output_size / (1024 * 1024)
            savings = result.savings_ratio * 100
            
            message = f"Original: {original_mb:.2f}MB → Compressed: {output_mb:.2f}MB (Saved {savings:.1f}%)"
            self.current_task.set_status("success", message)
            
        messagebox.showinfo("Success", f"Image compressed successfully!\nSaved to: {result.output_path}")
        
    def _on_compression_error(self, error_msg: str):
        """Handle compression error."""
        self.start_button.configure(state="normal", text="Start Compression")
        self.app.update_status("Compression failed")
        
        if self.current_task:
            self.current_task.set_status("error", f"Error: {error_msg}")
            
        messagebox.showerror("Compression Failed", error_msg)
        
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
        self.strip_meta_var.set(True)
        self.allow_large_var.set(False)
        
        # Clear results
        for widget in self.result_container.winfo_children():
            widget.destroy()
