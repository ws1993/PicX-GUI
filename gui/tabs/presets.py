"""Preset management tab."""
import customtkinter as ctk
from tkinter import messagebox, filedialog
from typing import Optional, Dict
import json
import os
from gui.styles.theme import COLORS, FONTS, SIZES
from gui.locales import PRESETS as PRESETS_LOCALE, COMMON


class PresetsTab(ctk.CTkFrame):
    """Tab for managing presets."""
    
    # Built-in presets
    BUILTIN_PRESETS = {
        "web": {
            "name": "Web",
            "description": PRESETS_LOCALE["builtin_web_desc"],
            "format": "webp",
            "quality": 82,
            "max_width": 1920,
            "strip_meta": True,
            "builtin": True
        },
        "blog": {
            "name": "Blog",
            "description": PRESETS_LOCALE["builtin_blog_desc"],
            "format": "webp",
            "quality": 78,
            "max_width": 1600,
            "strip_meta": True,
            "builtin": True
        },
        "avatar": {
            "name": "Avatar",
            "description": PRESETS_LOCALE["builtin_avatar_desc"],
            "format": "webp",
            "quality": 85,
            "max_width": 256,
            "max_height": 256,
            "strip_meta": True,
            "builtin": True
        },
        "lossless": {
            "name": "Lossless",
            "description": PRESETS_LOCALE["builtin_lossless_desc"],
            "format": "png",
            "quality": 100,
            "strip_meta": True,
            "builtin": True
        }
    }
    
    FORMATS = ["webp", "jpg", "png", "avif", "tiff"]
    
    def __init__(self, master, app_instance, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.app = app_instance
        self.custom_presets: Dict[str, dict] = {}
        self.current_editing = None
        
        # Load custom presets
        self._load_custom_presets()
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create UI
        self._create_header()
        self._create_preset_list()
        self._create_editor()
        
    def _create_header(self):
        """Create header section."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))
        
        # Title
        title = ctk.CTkLabel(
            header_frame,
            text=PRESETS_LOCALE["title"],
            font=FONTS["subheading"],
            text_color=COLORS["text"]
        )
        title.pack(side="left")
        
        # Import/Export buttons
        button_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        button_frame.pack(side="right")
        
        import_button = ctk.CTkButton(
            button_frame,
            text=PRESETS_LOCALE["import"],
            width=80,
            height=SIZES["button_height"],
            command=self._import_presets,
            fg_color=COLORS["info"],
            hover_color="#1976D2"
        )
        import_button.pack(side="left", padx=5)
        
        export_button = ctk.CTkButton(
            button_frame,
            text=PRESETS_LOCALE["export"],
            width=80,
            height=SIZES["button_height"],
            command=self._export_presets,
            fg_color=COLORS["success"],
            hover_color="#388E3C"
        )
        export_button.pack(side="left", padx=5)
        
    def _create_preset_list(self):
        """Create preset list section."""
        list_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=SIZES["corner_radius"])
        list_frame.grid(row=1, column=0, sticky="nsew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        # Title
        title = ctk.CTkLabel(
            list_frame,
            text=PRESETS_LOCALE["available_presets"],
            font=FONTS["subheading"],
            text_color=COLORS["text"]
        )
        title.pack(anchor="w", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))
        
        # Preset list container
        self.preset_list_container = ctk.CTkScrollableFrame(
            list_frame,
            fg_color="transparent"
        )
        self.preset_list_container.pack(fill="both", expand=True, padx=SIZES["padding"], pady=(0, SIZES["padding"]))
        
        # Populate preset list
        self._populate_preset_list()
        
    def _populate_preset_list(self):
        """Populate the preset list."""
        # Clear existing items
        for widget in self.preset_list_container.winfo_children():
            widget.destroy()
            
        # Show built-in presets
        builtin_label = ctk.CTkLabel(
            self.preset_list_container,
            text=PRESETS_LOCALE["builtin_presets"],
            font=FONTS["body_bold"],
            text_color=COLORS["text_muted"]
        )
        builtin_label.pack(fill="x", pady=(0, 5))
        
        for preset_id, preset_data in self.BUILTIN_PRESETS.items():
            self._add_preset_item(preset_id, preset_data, builtin=True)
            
        # Show custom presets
        if self.custom_presets:
            custom_label = ctk.CTkLabel(
                self.preset_list_container,
                text=PRESETS_LOCALE["custom_presets"],
                font=FONTS["body_bold"],
                text_color=COLORS["text_muted"]
            )
            custom_label.pack(fill="x", pady=(10, 5))
            
            for preset_id, preset_data in self.custom_presets.items():
                self._add_preset_item(preset_id, preset_data, builtin=False)
                
    def _add_preset_item(self, preset_id: str, preset_data: dict, builtin: bool = False):
        """Add a preset item to the list."""
        item_frame = ctk.CTkFrame(
            self.preset_list_container,
            fg_color=COLORS["surface_light"],
            corner_radius=4
        )
        item_frame.pack(fill="x", pady=2)
        
        # Info container
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)
        
        # Preset name
        name_label = ctk.CTkLabel(
            info_frame,
            text=preset_data.get("name", preset_id),
            font=FONTS["body_bold"],
            text_color=COLORS["text"],
            anchor="w"
        )
        name_label.pack(fill="x")
        
        # Description
        desc = preset_data.get("description", "")
        if desc:
            desc_label = ctk.CTkLabel(
                info_frame,
                text=desc,
                font=FONTS["small"],
                text_color=COLORS["text_muted"],
                anchor="w"
            )
            desc_label.pack(fill="x")
            
        # Buttons
        button_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=10, pady=5)
        
        # Edit button
        edit_button = ctk.CTkButton(
            button_frame,
            text=PRESETS_LOCALE["edit"],
            width=60,
            height=25,
            command=lambda pid=preset_id: self._edit_preset(pid),
            fg_color=COLORS["info"],
            hover_color="#1976D2",
            font=FONTS["small"]
        )
        edit_button.pack(side="left", padx=2)
        
        # Delete button (only for custom presets)
        if not builtin:
            delete_button = ctk.CTkButton(
                button_frame,
                text=PRESETS_LOCALE["delete"],
                width=60,
                height=25,
                command=lambda pid=preset_id: self._delete_preset(pid),
                fg_color=COLORS["error"],
                hover_color="#D32F2F",
                font=FONTS["small"]
            )
            delete_button.pack(side="left", padx=2)
            
    def _create_editor(self):
        """Create preset editor section."""
        editor_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=SIZES["corner_radius"])
        editor_frame.grid(row=2, column=0, sticky="ew", padx=SIZES["padding"], pady=(SIZES["padding_small"], SIZES["padding"]))
        
        # Title with action buttons
        title_frame = ctk.CTkFrame(editor_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))
        
        self.editor_title = ctk.CTkLabel(
            title_frame,
            text=PRESETS_LOCALE["create_new"],
            font=FONTS["subheading"],
            text_color=COLORS["text"]
        )
        self.editor_title.pack(side="left")
        
        # Action buttons
        button_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        button_frame.pack(side="right")
        
        self.save_button = ctk.CTkButton(
            button_frame,
            text=PRESETS_LOCALE["save"],
            width=80,
            height=SIZES["button_height"],
            command=self._save_preset,
            fg_color=COLORS["success"],
            hover_color="#388E3C"
        )
        self.save_button.pack(side="left", padx=5)
        
        self.cancel_button = ctk.CTkButton(
            button_frame,
            text=PRESETS_LOCALE["cancel"],
            width=80,
            height=SIZES["button_height"],
            command=self._cancel_edit,
            fg_color=COLORS["text_muted"],
            hover_color=COLORS["border"]
        )
        self.cancel_button.pack(side="left", padx=5)
        
        # Form
        form_frame = ctk.CTkFrame(editor_frame, fg_color="transparent")
        form_frame.pack(fill="x", padx=SIZES["padding"], pady=(0, SIZES["padding"]))
        form_frame.grid_columnconfigure(1, weight=1)
        
        current_row = 0
        
        # Preset ID
        id_label = ctk.CTkLabel(form_frame, text=PRESETS_LOCALE["preset_id"], font=FONTS["body"])
        id_label.grid(row=current_row, column=0, sticky="w", padx=(0, SIZES["padding_small"]), pady=5)

        self.preset_id_var = ctk.StringVar()
        self.id_entry = ctk.CTkEntry(
            form_frame,
            textvariable=self.preset_id_var,
            placeholder_text=PRESETS_LOCALE["id_placeholder"],
            height=SIZES["entry_height"]
        )
        self.id_entry.grid(row=current_row, column=1, sticky="ew", pady=5)
        current_row += 1

        # Name
        name_label = ctk.CTkLabel(form_frame, text=PRESETS_LOCALE["name"], font=FONTS["body"])
        name_label.grid(row=current_row, column=0, sticky="w", padx=(0, SIZES["padding_small"]), pady=5)

        self.name_var = ctk.StringVar()
        name_entry = ctk.CTkEntry(
            form_frame,
            textvariable=self.name_var,
            placeholder_text=PRESETS_LOCALE["name_placeholder"],
            height=SIZES["entry_height"]
        )
        name_entry.grid(row=current_row, column=1, sticky="ew", pady=5)
        current_row += 1

        # Description
        desc_label = ctk.CTkLabel(form_frame, text=PRESETS_LOCALE["description"], font=FONTS["body"])
        desc_label.grid(row=current_row, column=0, sticky="nw", padx=(0, SIZES["padding_small"]), pady=5)

        self.desc_var = ctk.StringVar()
        desc_entry = ctk.CTkEntry(
            form_frame,
            textvariable=self.desc_var,
            placeholder_text=PRESETS_LOCALE["desc_placeholder"],
            height=SIZES["entry_height"]
        )
        desc_entry.grid(row=current_row, column=1, sticky="ew", pady=5)
        current_row += 1

        # Format
        format_label = ctk.CTkLabel(form_frame, text=PRESETS_LOCALE["format"], font=FONTS["body"])
        format_label.grid(row=current_row, column=0, sticky="w", padx=(0, SIZES["padding_small"]), pady=5)
        
        self.format_var = ctk.StringVar(value="webp")
        format_menu = ctk.CTkOptionMenu(
            form_frame,
            variable=self.format_var,
            values=self.FORMATS
        )
        format_menu.grid(row=current_row, column=1, sticky="ew", pady=5)
        current_row += 1
        
        # Quality
        quality_label = ctk.CTkLabel(form_frame, text=PRESETS_LOCALE["quality"], font=FONTS["body"])
        quality_label.grid(row=current_row, column=0, sticky="w", padx=(0, SIZES["padding_small"]), pady=5)
        
        quality_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        quality_container.grid(row=current_row, column=1, sticky="ew", pady=5)
        quality_container.grid_columnconfigure(0, weight=1)
        
        self.quality_var = ctk.IntVar(value=82)
        quality_slider = ctk.CTkSlider(
            quality_container,
            from_=1,
            to=100,
            variable=self.quality_var,
            number_of_steps=99,
            progress_color=COLORS["primary"]
        )
        quality_slider.grid(row=0, column=0, sticky="ew", padx=(0, SIZES["padding_small"]))
        
        self.quality_label = ctk.CTkLabel(quality_container, text="82", font=FONTS["body_bold"], width=40)
        self.quality_label.grid(row=0, column=1)
        self.quality_var.trace_add("write", lambda *args: self.quality_label.configure(text=str(self.quality_var.get())))
        current_row += 1
        
        # Max width
        width_label = ctk.CTkLabel(form_frame, text=PRESETS_LOCALE["max_width"], font=FONTS["body"])
        width_label.grid(row=current_row, column=0, sticky="w", padx=(0, SIZES["padding_small"]), pady=5)

        self.max_width_var = ctk.StringVar()
        width_entry = ctk.CTkEntry(
            form_frame,
            textvariable=self.max_width_var,
            placeholder_text=PRESETS_LOCALE["leave_empty"],
            height=SIZES["entry_height"]
        )
        width_entry.grid(row=current_row, column=1, sticky="ew", pady=5)
        current_row += 1

        # Max height
        height_label = ctk.CTkLabel(form_frame, text=PRESETS_LOCALE["max_height"], font=FONTS["body"])
        height_label.grid(row=current_row, column=0, sticky="w", padx=(0, SIZES["padding_small"]), pady=5)

        self.max_height_var = ctk.StringVar()
        height_entry = ctk.CTkEntry(
            form_frame,
            textvariable=self.max_height_var,
            placeholder_text=PRESETS_LOCALE["leave_empty"],
            height=SIZES["entry_height"]
        )
        height_entry.grid(row=current_row, column=1, sticky="ew", pady=5)
        current_row += 1

        # Strip metadata
        self.strip_meta_var = ctk.BooleanVar(value=True)
        strip_meta_check = ctk.CTkCheckBox(
            form_frame,
            text=PRESETS_LOCALE["strip_metadata"],
            variable=self.strip_meta_var,
            font=FONTS["body"]
        )
        strip_meta_check.grid(row=current_row, column=0, columnspan=2, sticky="w", pady=5)
        
    def _edit_preset(self, preset_id: str):
        """Edit a preset."""
        # Get preset data
        if preset_id in self.BUILTIN_PRESETS:
            preset_data = self.BUILTIN_PRESETS[preset_id]
        elif preset_id in self.custom_presets:
            preset_data = self.custom_presets[preset_id]
        else:
            return
            
        # Fill form
        self.current_editing = preset_id
        self.preset_id_var.set(preset_id)
        self.id_entry.configure(state="disabled")  # Can't change ID
        self.name_var.set(preset_data.get("name", ""))
        self.desc_var.set(preset_data.get("description", ""))
        self.format_var.set(preset_data.get("format", "webp"))
        self.quality_var.set(preset_data.get("quality", 82))
        self.max_width_var.set(str(preset_data.get("max_width", "")))
        self.max_height_var.set(str(preset_data.get("max_height", "")))
        self.strip_meta_var.set(preset_data.get("strip_meta", True))
        
        # Update title
        self.editor_title.configure(text=PRESETS_LOCALE["edit_preset"].format(preset_data.get('name', preset_id)))
        
    def _cancel_edit(self):
        """Cancel editing."""
        self.current_editing = None
        self.preset_id_var.set("")
        self.id_entry.configure(state="normal")
        self.name_var.set("")
        self.desc_var.set("")
        self.format_var.set("webp")
        self.quality_var.set(82)
        self.max_width_var.set("")
        self.max_height_var.set("")
        self.strip_meta_var.set(True)
        
        # Reset title
        self.editor_title.configure(text=PRESETS_LOCALE["create_new"])
        
    def _save_preset(self):
        """Save the current preset."""
        # Get values
        preset_id = self.preset_id_var.get().strip()
        name = self.name_var.get().strip()
        desc = self.desc_var.get().strip()
        format_val = self.format_var.get()
        quality = self.quality_var.get()
        
        # Validate
        if not preset_id:
            messagebox.showerror(PRESETS_LOCALE["error"], PRESETS_LOCALE["input_preset_id"])
            return

        if not name:
            messagebox.showerror(PRESETS_LOCALE["error"], PRESETS_LOCALE["input_preset_name"])
            return

        # Check if trying to edit built-in
        if self.current_editing and self.current_editing in self.BUILTIN_PRESETS:
            messagebox.showerror(PRESETS_LOCALE["error"], PRESETS_LOCALE["cannot_edit_builtin"])
            return
            
        # Build preset data
        preset_data = {
            "name": name,
            "description": desc,
            "format": format_val,
            "quality": quality,
            "strip_meta": self.strip_meta_var.get(),
            "builtin": False
        }
        
        # Add optional fields
        if self.max_width_var.get():
            try:
                preset_data["max_width"] = int(self.max_width_var.get())
            except ValueError:
                messagebox.showerror(PRESETS_LOCALE["error"], PRESETS_LOCALE["width_must_be_int"])
                return

        if self.max_height_var.get():
            try:
                preset_data["max_height"] = int(self.max_height_var.get())
            except ValueError:
                messagebox.showerror(PRESETS_LOCALE["error"], PRESETS_LOCALE["height_must_be_int"])
                return
                
        # Save
        self.custom_presets[preset_id] = preset_data
        self._save_custom_presets()
        
        # Update UI
        self._populate_preset_list()
        self._cancel_edit()
        
        messagebox.showinfo(PRESETS_LOCALE["success"], PRESETS_LOCALE["preset_saved_msg"].format(name))

    def _delete_preset(self, preset_id: str):
        """Delete a custom preset."""
        if preset_id in self.BUILTIN_PRESETS:
            messagebox.showerror(PRESETS_LOCALE["error"], PRESETS_LOCALE["cannot_delete_builtin"])
            return
            
        if preset_id not in self.custom_presets:
            return
            
        # Confirm
        preset_name = self.custom_presets[preset_id].get("name", preset_id)
        if not messagebox.askyesno(PRESETS_LOCALE["confirm_delete_title"], PRESETS_LOCALE["confirm_delete_msg"].format(preset_name)):
            return
            
        # Delete
        del self.custom_presets[preset_id]
        self._save_custom_presets()
        
        # Update UI
        self._populate_preset_list()
        
        messagebox.showinfo(PRESETS_LOCALE["success"], PRESETS_LOCALE["preset_deleted_msg"].format(preset_name))
        
    def _load_custom_presets(self):
        """Load custom presets from file."""
        config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "config")
        presets_file = os.path.join(config_dir, "custom_presets.json")
        
        if os.path.exists(presets_file):
            try:
                with open(presets_file, 'r', encoding='utf-8') as f:
                    self.custom_presets = json.load(f)
            except Exception as e:
                print(f"Error loading custom presets: {e}")
                self.custom_presets = {}
                
    def _save_custom_presets(self):
        """Save custom presets to file."""
        config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "config")
        os.makedirs(config_dir, exist_ok=True)
        
        presets_file = os.path.join(config_dir, "custom_presets.json")
        
        try:
            with open(presets_file, 'w', encoding='utf-8') as f:
                json.dump(self.custom_presets, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving custom presets: {e}")
            
    def _import_presets(self):
        """Import presets from JSON file."""
        file_path = filedialog.askopenfilename(
            title=PRESETS_LOCALE["import_presets"],
            filetypes=[(PRESETS_LOCALE["json_files"], "*.json"), (PRESETS_LOCALE["all_files"], "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported = json.load(f)
                
            if not isinstance(imported, dict):
                messagebox.showerror(PRESETS_LOCALE["error"], PRESETS_LOCALE["invalid_preset_file"])
                return
                
            # Merge with existing presets
            count = 0
            for preset_id, preset_data in imported.items():
                if preset_id not in self.BUILTIN_PRESETS:
                    self.custom_presets[preset_id] = preset_data
                    count += 1
                    
            self._save_custom_presets()
            self._populate_preset_list()
            
            messagebox.showinfo(PRESETS_LOCALE["success"], PRESETS_LOCALE["import_success"].format(count))

        except Exception as e:
            messagebox.showerror(PRESETS_LOCALE["import_failed"], PRESETS_LOCALE["import_failed_detail"].format(str(e)))
            
    def _export_presets(self):
        """Export custom presets to JSON file."""
        if not self.custom_presets:
            messagebox.showinfo(PRESETS_LOCALE["hint"], PRESETS_LOCALE["no_custom_export"])
            return
            
        file_path = filedialog.asksaveasfilename(
            title=PRESETS_LOCALE["export_presets"],
            defaultextension=".json",
            filetypes=[(PRESETS_LOCALE["json_files"], "*.json"), (PRESETS_LOCALE["all_files"], "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.custom_presets, f, indent=2, ensure_ascii=False)
                
            messagebox.showinfo(PRESETS_LOCALE["success"], PRESETS_LOCALE["export_success"].format(file_path))

        except Exception as e:
            messagebox.showerror(PRESETS_LOCALE["export_failed"], PRESETS_LOCALE["export_failed_detail"].format(str(e)))
