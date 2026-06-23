"""File and directory selector widget."""
import customtkinter as ctk
from tkinter import filedialog
from typing import Optional, Callable, Literal
from gui.styles.theme import COLORS, FONTS, SIZES, SPACING
from gui.locales import FILESELECTOR


class FileSelector(ctk.CTkFrame):
    """Widget for selecting files or directories with a browse button."""
    
    def __init__(
        self,
        master,
        mode: Literal["file", "directory", "save"] = "file",
        label_text: str = "Select file:",
        filetypes: Optional[list] = None,
        on_change: Optional[Callable[[str], None]] = None,
        **kwargs
    ):
        """
        Initialize FileSelector.
        
        Args:
            master: Parent widget
            mode: "file" for file selection, "directory" for folder, "save" for save dialog
            label_text: Label text to display
            filetypes: List of file type tuples for file dialog (e.g., [("Images", "*.png *.jpg")])
            on_change: Callback function when path changes
        """
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.mode = mode
        self.filetypes = filetypes or [(FILESELECTOR["all_files"], "*.*")]
        self.on_change_callback = on_change
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        
        # Label
        self.label = ctk.CTkLabel(
            self,
            text=label_text,
            font=FONTS["body"],
            text_color=COLORS["text"]
        )
        self.label.grid(row=0, column=0, padx=(0, SIZES["padding_small"]), sticky="w")
        
        # Path entry
        self.path_var = ctk.StringVar()
        self.path_entry = ctk.CTkEntry(
            self,
            textvariable=self.path_var,
            font=FONTS["body"],
            height=SIZES["entry_height"],
            placeholder_text=FILESELECTOR["no_file"] if mode != "directory" else FILESELECTOR["no_dir"]
        )
        self.path_entry.grid(row=0, column=1, padx=SIZES["padding_small"], sticky="ew")
        
        # Bind change event
        self.path_var.trace_add("write", self._on_path_change)
        
        # Browse button
        self.browse_button = ctk.CTkButton(
            self,
            text=FILESELECTOR["browse"],
            width=100,
            height=SIZES["button_height"],
            command=self._browse,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            font=FONTS["button"]
        )
        self.browse_button.grid(row=0, column=2, padx=(SIZES["padding_small"], 0))
        
    def _browse(self):
        """Open file/directory dialog."""
        if self.mode == "file":
            path = filedialog.askopenfilename(
                title=FILESELECTOR["dialog_select"],
                filetypes=self.filetypes
            )
        elif self.mode == "directory":
            path = filedialog.askdirectory(
                title=FILESELECTOR["dialog_dir"]
            )
        elif self.mode == "save":
            path = filedialog.asksaveasfilename(
                title=FILESELECTOR["dialog_save"],
                filetypes=self.filetypes
            )
        else:
            path = ""
            
        if path:
            self.path_var.set(path)
            
    def _on_path_change(self, *args):
        """Handle path change event."""
        if self.on_change_callback:
            self.on_change_callback(self.path_var.get())
            
    def get(self) -> str:
        """Get current path."""
        return self.path_var.get()
    
    def set(self, path: str):
        """Set path."""
        self.path_var.set(path)
        
    def clear(self):
        """Clear path."""
        self.path_var.set("")
