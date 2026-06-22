"""Drop zone widget for drag and drop file selection."""
import customtkinter as ctk
from typing import Optional, Callable, List
from gui.styles.theme import COLORS, FONTS, SIZES, SPACING


class DropZone(ctk.CTkFrame):
    """
    Widget for drag and drop file selection.
    
    Note: Full drag-and-drop support requires tkinterdnd2, which will be integrated later.
    For now, this provides a visual drop zone with click-to-select functionality.
    """
    
    def __init__(
        self,
        master,
        on_files_dropped: Optional[Callable[[List[str]], None]] = None,
        accept_multiple: bool = True,
        accept_folders: bool = False,
        **kwargs
    ):
        """
        Initialize DropZone.
        
        Args:
            master: Parent widget
            on_files_dropped: Callback function when files are dropped/selected
            accept_multiple: Whether to accept multiple files
            accept_folders: Whether to accept folders
        """
        super().__init__(
            master,
            fg_color=COLORS["accent_tint"],
            border_color=COLORS["border"],
            border_width=2,
            corner_radius=SIZES["corner_radius"],
            **kwargs
        )
        
        self.on_files_dropped = on_files_dropped
        self.accept_multiple = accept_multiple
        self.accept_folders = accept_folders
        self.files: List[str] = []
        
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Icon label (placeholder - could use emoji or icon)
        self.icon_label = ctk.CTkLabel(
            container,
            text="📁",
            font=("Arial", 48),
        )
        self.icon_label.grid(row=0, column=0, pady=(0, 20))
        
        # Instruction label
        instruction = "Drag and drop files or folders here"
        if not accept_folders:
            instruction = "Drag and drop files here"
        elif accept_folders and not accept_multiple:
            instruction = "Drag and drop a folder here"
            
        self.instruction_label = ctk.CTkLabel(
            container,
            text=instruction,
            font=FONTS["body_bold"],
            text_color=COLORS["text"]
        )
        self.instruction_label.grid(row=1, column=0)
        
        # Or label
        or_label = ctk.CTkLabel(
            container,
            text="or",
            font=FONTS["small"],
            text_color=COLORS["text_muted"]
        )
        or_label.grid(row=2, column=0, pady=10)
        
        # Browse button
        button_text = "Browse Files"
        if accept_folders and not accept_multiple:
            button_text = "Browse Folder"
        elif accept_folders:
            button_text = "Browse Files/Folders"
            
        self.browse_button = ctk.CTkButton(
            container,
            text=button_text,
            width=150,
            height=SIZES["button_height"],
            command=self._browse,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            font=FONTS["button"]
        )
        self.browse_button.grid(row=3, column=0, pady=(0, 10))
        
        # File count label
        self.file_count_label = ctk.CTkLabel(
            container,
            text="",
            font=FONTS["small"],
            text_color=COLORS["text_muted"]
        )
        self.file_count_label.grid(row=4, column=0)
        
        # Bind events for visual feedback
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        # TODO: Add tkinterdnd2 drag-and-drop support
        # self.drop_target_register(DND_FILES)
        # self.dnd_bind('<<Drop>>', self._on_drop)
        
    def _browse(self):
        """Open file/folder browser."""
        from tkinter import filedialog
        
        if self.accept_folders and not self.accept_multiple:
            path = filedialog.askdirectory(title="Select a folder")
            if path:
                self._handle_files([path])
        elif self.accept_multiple:
            paths = filedialog.askopenfilenames(title="Select files")
            if paths:
                self._handle_files(list(paths))
        else:
            path = filedialog.askopenfilename(title="Select a file")
            if path:
                self._handle_files([path])
                
    def _handle_files(self, file_paths: List[str]):
        """Handle selected files."""
        self.files = file_paths
        
        # Update file count label
        count = len(file_paths)
        if count == 1:
            self.file_count_label.configure(text=f"Selected: {file_paths[0]}")
        else:
            self.file_count_label.configure(text=f"Selected: {count} files")
            
        # Trigger callback
        if self.on_files_dropped:
            self.on_files_dropped(file_paths)
            
    def _on_enter(self, event):
        """Visual feedback when mouse enters."""
        self.configure(border_color=COLORS["primary"])
        
    def _on_leave(self, event):
        """Visual feedback when mouse leaves."""
        self.configure(border_color=COLORS["border"])
        
    def get_files(self) -> List[str]:
        """Get list of selected files."""
        return self.files
    
    def clear(self):
        """Clear selected files."""
        self.files = []
        self.file_count_label.configure(text="")
