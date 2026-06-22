"""PicX GUI Main Application."""
import customtkinter as ctk
from gui.locales import MAIN_WINDOW, TABS
from gui.styles.theme import COLORS, FONTS, SIZES, apply_theme


class PicXApp(ctk.CTk):
    """Main application window for PicX GUI."""
    
    def __init__(self):
        super().__init__()
        
        # Apply theme
        apply_theme("light")
        
        # Configure window
        self.title(MAIN_WINDOW["title"])
        self.geometry(f"{SIZES['window_width']}x{SIZES['window_height']}")
        self.minsize(SIZES["min_width"], SIZES["min_height"])
        
        # Set window icon (if available)
        try:
            self.iconbitmap("assets/icon.ico")
        except:
            pass
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create header
        self._create_header()
        
        # Create tab view
        self._create_tab_view()
        
        # Create status bar
        self._create_status_bar()
        
        # Bind keyboard shortcuts
        self._bind_shortcuts()
        
    def _create_header(self):
        """Create application header."""
        header = ctk.CTkFrame(self, fg_color=COLORS["dark_block"], corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)
        
        # App title
        title = ctk.CTkLabel(
            header,
            text=MAIN_WINDOW["title"],
            font=FONTS["heading"],
            text_color="white"
        )
        title.grid(row=0, column=0, padx=SIZES["padding"], pady=(SIZES["padding"], 5))
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            header,
            text=MAIN_WINDOW["subtitle"],
            font=FONTS["small"],
            text_color="#AAAAAA"
        )
        subtitle.grid(row=1, column=0, padx=SIZES["padding"], pady=(0, SIZES["padding"]))
        
        # Theme toggle button
        self.theme_mode = "light"
        self.theme_btn = ctk.CTkButton(
            header,
            text=MAIN_WINDOW["theme_dark"],
            width=100,
            height=30,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            command=self._toggle_theme
        )
        self.theme_btn.grid(row=0, column=1, rowspan=2, padx=SIZES["padding"], pady=SIZES["padding"], sticky="e")
        
    def _create_tab_view(self):
        """Create tab view for different features."""
        self.tab_view = ctk.CTkTabview(
            self,
            fg_color=COLORS["surface"],
            segmented_button_fg_color=COLORS["border"],
            segmented_button_selected_color=COLORS["primary"],
            segmented_button_selected_hover_color=COLORS["primary_hover"],
            corner_radius=SIZES["corner_radius"]
        )
        self.tab_view.grid(row=1, column=0, sticky="nsew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        # Add tabs
        self.tab_single = self.tab_view.add(TABS["single_image"])
        self.tab_batch = self.tab_view.add(TABS["batch_process"])
        self.tab_tile = self.tab_view.add(TABS["tile_images"])
        self.tab_doctor = self.tab_view.add(TABS["environment_check"])
        self.tab_presets = self.tab_view.add(TABS["presets"])
        
        # Populate tabs with content
        self._populate_tabs()
        
    def _populate_tabs(self):
        """Populate tabs with content."""
        from gui.tabs.single_image_optimized import SingleImageTabOptimized
        from gui.tabs.batch import BatchTab
        from gui.tabs.tile import TileTab
        from gui.tabs.doctor import DoctorTab
        from gui.tabs.presets import PresetsTab
        
        # Single Image tab
        single_tab = SingleImageTabOptimized(self.tab_single, app_instance=self)
        single_tab.pack(fill="both", expand=True)
        
        # Batch tab
        batch_tab = BatchTab(self.tab_batch, app_instance=self)
        batch_tab.pack(fill="both", expand=True)
        
        # Tile tab
        tile_tab = TileTab(self.tab_tile, app_instance=self)
        tile_tab.pack(fill="both", expand=True)
        
        # Doctor tab
        doctor_tab = DoctorTab(self.tab_doctor, app_instance=self)
        doctor_tab.pack(fill="both", expand=True)
        
        # Presets tab
        presets_tab = PresetsTab(self.tab_presets, app_instance=self)
        presets_tab.pack(fill="both", expand=True)
        
    def _create_status_bar(self):
        """Create status bar at bottom."""
        status_bar = ctk.CTkFrame(self, fg_color=COLORS["border"], corner_radius=0, height=25)
        status_bar.grid(row=2, column=0, sticky="ew")
        status_bar.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(
            status_bar,
            text=MAIN_WINDOW["status_ready"],
            font=FONTS["small"],
            text_color=COLORS["text_muted"]
        )
        self.status_label.grid(row=0, column=0, padx=10, pady=2, sticky="w")
        
    def _bind_shortcuts(self):
        """Bind keyboard shortcuts."""
        self.bind("<Control-o>", lambda e: self._open_file())
        self.bind("<Control-Shift-KeyPress-O>", lambda e: self._open_directory())
        self.bind("<Control-t>", lambda e: self._switch_to_tab(TABS["tile_images"]))
        self.bind("<Control-d>", lambda e: self._switch_to_tab(TABS["environment_check"]))
        self.bind("<Control-p>", lambda e: self._switch_to_tab(TABS["presets"]))
        self.bind("<Control-q>", lambda e: self.quit())
        self.bind("<F1>", lambda e: self._show_help())
        self.bind("<F5>", lambda e: self._refresh())
        
    def _toggle_theme(self):
        """Toggle between light and dark theme."""
        if self.theme_mode == "light":
            self.theme_mode = "dark"
            apply_theme("dark")
            self.theme_btn.configure(text=MAIN_WINDOW["theme_light"])
        else:
            self.theme_mode = "light"
            apply_theme("light")
            self.theme_btn.configure(text=MAIN_WINDOW["theme_dark"])
            
    def _switch_to_tab(self, tab_name):
        """Switch to specified tab."""
        self.tab_view.set(tab_name)
        
    def _open_file(self):
        """Open file dialog."""
        from tkinter import filedialog
        filetypes = [
            ("图片文件", "*.png *.jpg *.jpeg *.webp *.avif *.tif *.tiff"),
            ("所有文件", "*.*")
        ]
        filedialog.askopenfilename(filetypes=filetypes)
        
    def _open_directory(self):
        """Open directory dialog."""
        from tkinter import filedialog
        filedialog.askdirectory()
        
    def _show_help(self):
        """Show help dialog."""
        from tkinter import messagebox
        messagebox.showinfo(
            "帮助",
            "PicX 图片优化工具\n\n"
            "快捷键:\n"
            "  Ctrl+O - 打开文件\n"
            "  Ctrl+Shift+O - 打开目录\n"
            "  Ctrl+T - 切片模式\n"
            "  Ctrl+D - 环境检查\n"
            "  Ctrl+P - 预设管理\n"
            "  Ctrl+Q - 退出\n"
            "  F1 - 帮助\n"
            "  F5 - 刷新"
        )
        
    def _refresh(self):
        """Refresh current view."""
        self.status_label.configure(text="刷新中...")
        self.after(1000, lambda: self.status_label.configure(text=MAIN_WINDOW["status_ready"]))
        
    def set_status(self, text):
        """Set status bar text."""
        self.status_label.configure(text=text)
