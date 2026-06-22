"""Large image tiling tab."""
import customtkinter as ctk
from tkinter import messagebox, filedialog
from typing import Optional
import json
from gui.styles.theme import COLORS, FONTS, SIZES
from gui.widgets.file_selector import FileSelector
from gui.widgets.progress_item import ProgressItem
from gui.utils.validators import (
    validate_quality,
    validate_tile_size,
    validate_file_path
)
from gui.locales import COMMON, TILE


class TileTab(ctk.CTkFrame):
    """Tab for large image tiling."""
    
    FORMATS = ["webp", "jpg", "png"]
    BACKENDS = ["auto", "pillow", "pyvips"]
    
    def __init__(self, master, app_instance, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.app = app_instance
        self.current_task = None
        self.manifest = None
        
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
            text=COMMON["input_output"],
            font=FONTS["subheading"],
            text_color=COLORS["text"]
        )
        title.grid(row=0, column=0, sticky="w", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))
        
        # Input file selector
        self.input_selector = FileSelector(
            input_frame,
            mode="file",
            label_text=TILE["input_image"],
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.webp *.avif *.tif *.tiff"),
                ("All files", "*.*")
            ]
        )
        self.input_selector.grid(row=1, column=0, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        # Output directory selector
        self.output_selector = FileSelector(
            input_frame,
            mode="directory",
            label_text=TILE["tile_output_dir"] + ":"
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
            text=TILE["tile_params"],
            font=FONTS["subheading"],
            text_color=COLORS["text"]
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))
        
        current_row = 1
        
        # Tile size
        size_label = ctk.CTkLabel(params_frame, text=TILE["tile_size"], font=FONTS["body"])
        size_label.grid(row=current_row, column=0, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        self.tile_size_var = ctk.StringVar(value="1024")
        size_entry = ctk.CTkEntry(
            params_frame,
            textvariable=self.tile_size_var,
            placeholder_text=TILE["tile_size_hint"],
            height=SIZES["entry_height"]
        )
        size_entry.grid(row=current_row, column=1, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
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
        
        # Pyramid checkbox
        self.pyramid_var = ctk.BooleanVar(value=True)
        pyramid_check = ctk.CTkCheckBox(
            params_frame,
            text=TILE["pyramid"],
            variable=self.pyramid_var,
            font=FONTS["body"]
        )
        pyramid_check.grid(row=current_row, column=0, columnspan=2, sticky="w", padx=SIZES["padding"], pady=SIZES["padding_small"])
        current_row += 1
        
        # Info text
        info_text = TILE["pyramid_info"]
        info_label = ctk.CTkLabel(
            params_frame,
            text=info_text,
            font=FONTS["small"],
            text_color=COLORS["text_muted"],
            wraplength=400,
            justify="left"
        )
        info_label.grid(row=current_row, column=0, columnspan=2, sticky="w", padx=SIZES["padding"], pady=(0, SIZES["padding"]))
        
    def _create_action_section(self):
        """Create action buttons section."""
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=2, column=0, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        # Start button
        self.start_button = ctk.CTkButton(
            action_frame,
            text=TILE["start_tiling"],
            height=SIZES["button_height"] + 10,
            command=self._start_tiling,
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
        
        # Title
        title = ctk.CTkLabel(
            self.result_frame,
            text=COMMON["result"],
            font=FONTS["subheading"],
            text_color=COLORS["text"]
        )
        title.pack(anchor="w", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))
        
        # Progress container
        self.progress_container = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        self.progress_container.pack(fill="x", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        # Stats container
        self.stats_container = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        self.stats_container.pack(fill="x", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        # Manifest preview button (initially hidden)
        self.manifest_button = ctk.CTkButton(
            self.result_frame,
            text=TILE["view_manifest"],
            command=self._show_manifest,
            fg_color=COLORS["info"],
            hover_color="#1976D2"
        )
        
    def _validate_params(self) -> tuple[bool, Optional[str]]:
        """Validate all parameters."""
        # Validate input path
        input_path = self.input_selector.get()
        is_valid, error = validate_file_path(input_path, must_exist=True)
        if not is_valid:
            return False, error
            
        # Validate output directory
        output_dir = self.output_selector.get()
        if not output_dir:
            return False, TILE["select_output_dir"]
            
        # Validate tile size
        if self.tile_size_var.get():
            try:
                tile_size = int(self.tile_size_var.get())
                is_valid, error = validate_tile_size(tile_size)
                if not is_valid:
                    return False, error
            except ValueError:
                return False, TILE["invalid_tile_size"]
        else:
            return False, TILE["enter_tile_size"]
            
        # Validate quality
        is_valid, error = validate_quality(self.quality_var.get())
        if not is_valid:
            return False, error
            
        return True, None
        
    def _start_tiling(self):
        """Start the tiling process."""
        # Validate parameters
        is_valid, error = self._validate_params()
        if not is_valid:
            messagebox.showerror(TILE["validation_error"], error)
            return
            
        # Collect parameters
        params = self._collect_params()
        
        # Update UI
        self.start_button.configure(state="disabled", text=TILE["processing"])
        self.app.update_status(TILE["tiling"])
        
        # Clear previous results
        for widget in self.progress_container.winfo_children():
            widget.destroy()
        for widget in self.stats_container.winfo_children():
            widget.destroy()
        self.manifest_button.pack_forget()
        self.manifest = None
        
        # Create progress item
        self.current_task = ProgressItem(
            self.progress_container,
            task_name=f"{TILE['tile_task']}: {params['source']}",
            show_cancel=False
        )
        self.current_task.pack(fill="x", pady=SIZES["padding_small"])
        self.current_task.set_status("processing", TILE["tiling"])
        
        # Run tiling in background
        self._run_tiling(params)
        
    def _collect_params(self) -> dict:
        """Collect all parameters into a dictionary."""
        params = {
            "source": self.input_selector.get(),
            "out_dir": self.output_selector.get(),
            "tile_size": int(self.tile_size_var.get()),
            "format": self.format_var.get(),
            "quality": self.quality_var.get(),
            "backend": self.backend_var.get(),
            "pyramid": self.pyramid_var.get(),
        }
        
        return params
        
    def _run_tiling(self, params: dict):
        """Run tiling (placeholder - will be implemented with threading)."""
        import threading
        
        def worker():
            try:
                # Import PicX
                from picx import tile_image
                
                # Run tiling
                manifest = tile_image(**params)
                
                # Update UI on success
                self.after(0, lambda: self._on_tiling_complete(manifest))
            except Exception as e:
                # Update UI on error
                self.after(0, lambda: self._on_tiling_error(str(e)))
                
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        
    def _on_tiling_complete(self, manifest):
        """Handle successful tiling."""
        self.start_button.configure(state="normal", text=TILE["start_tiling"])
        self.app.update_status(TILE["tiling_completed"])
        
        self.manifest = manifest
        
        if self.current_task:
            self.current_task.set_status("success", TILE["tiling_completed"])
            
        # Count tiles
        tile_count = sum(len(level["tiles"]) for level in manifest["levels"])
        level_count = len(manifest["levels"])
        
        # Show stats
        stats_text = (
            f"原始尺寸: {manifest['original_width']} x {manifest['original_height']}\n"
            f"切片大小: {manifest['tile_size']} x {manifest['tile_size']}\n"
            f"缩放层级: {level_count}\n"
            f"总切片数: {tile_count}\n"
            f"输出格式: {manifest['format']}\n"
            f"后端: {manifest['backend']}"
        )
        
        stats_label = ctk.CTkLabel(
            self.stats_container,
            text=stats_text,
            font=FONTS["body"],
            text_color=COLORS["text"],
            justify="left"
        )
        stats_label.pack(anchor="w")
        
        # Show manifest button
        self.manifest_button.pack(pady=SIZES["padding_small"])
        
        messagebox.showinfo(
            TILE["tiling_completed"],
            f"成功生成 {tile_count} 个切片，分为 {level_count} 个层级。\n"
            f"输出目录: {self.output_selector.get()}"
        )
        
    def _on_tiling_error(self, error_msg: str):
        """Handle tiling error."""
        self.start_button.configure(state="normal", text=TILE["start_tiling"])
        self.app.update_status(TILE["failed"])
        
        if self.current_task:
            self.current_task.set_status("error", f"{TILE['error']}: {error_msg}")
            
        messagebox.showerror(TILE["failed"], f"{TILE['failed_detail']}:\n{error_msg}")
        
    def _show_manifest(self):
        """Show manifest.json content in a dialog."""
        if not self.manifest:
            return
            
        # Create dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("manifest.json")
        dialog.geometry("600x400")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        
        # Text widget to show manifest
        text_widget = ctk.CTkTextbox(
            dialog,
            font=("Courier", 12),
            wrap="word"
        )
        text_widget.pack(fill="both", expand=True, padx=SIZES["padding"], pady=SIZES["padding"])
        
        # Format manifest as JSON
        manifest_json = json.dumps(self.manifest, indent=2, ensure_ascii=False)
        text_widget.insert("1.0", manifest_json)
        text_widget.configure(state="disabled")
        
        # Close button
        close_button = ctk.CTkButton(
            dialog,
            text=TILE["close"],
            command=dialog.destroy
        )
        close_button.pack(pady=(0, SIZES["padding"]))
        
    def _clear_form(self):
        """Clear the form."""
        self.input_selector.clear()
        self.output_selector.clear()
        self.tile_size_var.set("1024")
        self.format_var.set("webp")
        self.quality_var.set(82)
        self.backend_var.set("auto")
        self.pyramid_var.set(True)
        
        # Clear results
        for widget in self.progress_container.winfo_children():
            widget.destroy()
        for widget in self.stats_container.winfo_children():
            widget.destroy()
        self.manifest_button.pack_forget()
        self.manifest = None
