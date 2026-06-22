"""Main application window for PicX GUI."""
import customtkinter as ctk
from gui.styles.theme import COLORS, FONTS, SIZES, apply_theme


class PicXApp(ctk.CTk):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        # Apply theme
        apply_theme("light")
        
        # Window configuration
        self.title("PicX GUI - Image Optimization Tool")
        self.geometry(f"{SIZES['window_width']}x{SIZES['window_height']}")
        self.minsize(SIZES['min_width'], SIZES['min_height'])
        
        # Configure grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create UI components
        self._create_header()
        self._create_tab_view()
        self._create_statusbar()
        
    def _create_header(self):
        """Create header with title and controls."""
        header_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="PicX",
            font=FONTS["heading"],
            text_color=COLORS["text"]
        )
        title_label.grid(row=0, column=0, padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Image Optimization Tool",
            font=FONTS["body"],
            text_color=COLORS["text_muted"]
        )
        subtitle_label.grid(row=0, column=1, padx=0, pady=SIZES["padding_small"], sticky="w")
        
        # Theme toggle button
        self.theme_button = ctk.CTkButton(
            header_frame,
            text="☀️ Light",
            width=100,
            height=SIZES["button_height"],
            command=self._toggle_theme,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"]
        )
        self.theme_button.grid(row=0, column=2, padx=SIZES["padding_small"], pady=SIZES["padding_small"])
        
        self.current_theme = "light"
        
    def _create_tab_view(self):
        """Create main tab view."""
        self.tab_view = ctk.CTkTabview(
            self,
            corner_radius=SIZES["corner_radius"],
            fg_color=COLORS["surface"]
        )
        self.tab_view.grid(
            row=1, 
            column=0, 
            padx=SIZES["padding"], 
            pady=(0, SIZES["padding"]), 
            sticky="nsew"
        )
        
        # Add tabs
        self.tab_single = self.tab_view.add("Single Image")
        self.tab_batch = self.tab_view.add("Batch Process")
        self.tab_tile = self.tab_view.add("Tile Large Images")
        self.tab_doctor = self.tab_view.add("Environment Check")
        self.tab_presets = self.tab_view.add("Presets")
        
        # Populate tabs with placeholder content
        self._populate_tabs()
        
    def _populate_tabs(self):
        """Populate tabs with content."""
        from gui.tabs.single_image import SingleImageTab
        
        # Single Image tab
        single_tab = SingleImageTab(self.tab_single, app_instance=self)
        single_tab.pack(fill="both", expand=True)
        
        # Batch tab placeholder
        label = ctk.CTkLabel(
            self.tab_batch,
            text="Batch Directory Processing\n(Coming soon)",
            font=FONTS["subheading"]
        )
        label.pack(pady=50)
        
        # Tile tab placeholder
        label = ctk.CTkLabel(
            self.tab_tile,
            text="Large Image Tiling\n(Coming soon)",
            font=FONTS["subheading"]
        )
        label.pack(pady=50)
        
        # Doctor tab placeholder
        label = ctk.CTkLabel(
            self.tab_doctor,
            text="Environment Diagnostics\n(Coming soon)",
            font=FONTS["subheading"]
        )
        label.pack(pady=50)
        
        # Presets tab placeholder
        label = ctk.CTkLabel(
            self.tab_presets,
            text="Preset Management\n(Coming soon)",
            font=FONTS["subheading"]
        )
        label.pack(pady=50)
        
    def _create_statusbar(self):
        """Create status bar at the bottom."""
        self.statusbar = ctk.CTkFrame(
            self,
            fg_color=COLORS["surface"],
            corner_radius=0,
            height=30
        )
        self.statusbar.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        self.statusbar.grid_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            self.statusbar,
            text="Ready",
            font=FONTS["small"],
            text_color=COLORS["text_muted"]
        )
        self.status_label.pack(side="left", padx=SIZES["padding"])
        
    def _toggle_theme(self):
        """Toggle between light and dark themes."""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        apply_theme(self.current_theme)
        
        # Update button text
        if self.current_theme == "dark":
            self.theme_button.configure(text="🌙 Dark")
        else:
            self.theme_button.configure(text="☀️ Light")
            
    def update_status(self, message: str):
        """Update status bar message."""
        self.status_label.configure(text=message)
