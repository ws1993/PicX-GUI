"""Progress item widget for displaying task progress."""
import customtkinter as ctk
from typing import Literal
from gui.styles.theme import COLORS, FONTS, SIZES, SPACING


class ProgressItem(ctk.CTkFrame):
    """Widget for displaying individual task progress."""
    
    def __init__(
        self,
        master,
        task_name: str = "Task",
        show_cancel: bool = True,
        on_cancel=None,
        **kwargs
    ):
        """
        Initialize ProgressItem.
        
        Args:
            master: Parent widget
            task_name: Name of the task
            show_cancel: Whether to show cancel button
            on_cancel: Callback for cancel button
        """
        super().__init__(
            master,
            fg_color=COLORS["surface_light"],
            corner_radius=SIZES["corner_radius"],
            border_width=1,
            border_color=COLORS["border"],
            **kwargs
        )
        
        self.task_name = task_name
        self.on_cancel = on_cancel
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        
        # Status icon
        self.status_icon = ctk.CTkLabel(
            self,
            text="⏳",
            font=("Arial", 16)
        )
        self.status_icon.grid(row=0, column=0, padx=SIZES["padding_small"], pady=SIZES["padding_small"])
        
        # Task info container
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="ew", padx=SIZES["padding_small"], pady=SIZES["padding_small"])
        info_frame.grid_columnconfigure(0, weight=1)
        
        # Task name label
        self.name_label = ctk.CTkLabel(
            info_frame,
            text=task_name,
            font=FONTS["body_bold"],
            text_color=COLORS["text"],
            anchor="w"
        )
        self.name_label.grid(row=0, column=0, sticky="w")
        
        # Status label
        self.status_label = ctk.CTkLabel(
            info_frame,
            text="Preparing...",
            font=FONTS["small"],
            text_color=COLORS["text_muted"],
            anchor="w"
        )
        self.status_label.grid(row=1, column=0, sticky="w")
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            info_frame,
            height=8,
            progress_color=COLORS["primary"]
        )
        self.progress_bar.grid(row=2, column=0, sticky="ew", pady=(5, 0))
        self.progress_bar.set(0)
        
        # Cancel button
        if show_cancel:
            self.cancel_button = ctk.CTkButton(
                self,
                text="✕",
                width=30,
                height=30,
                command=self._on_cancel_clicked,
                fg_color=COLORS["error"],
                hover_color="#D32F2F",
                font=FONTS["body_bold"]
            )
            self.cancel_button.grid(row=0, column=2, padx=SIZES["padding_small"])
        else:
            self.cancel_button = None
            
    def update_progress(self, progress: float, status_text: str = ""):
        """
        Update progress.
        
        Args:
            progress: Progress value between 0 and 1
            status_text: Status message
        """
        self.progress_bar.set(progress)
        if status_text:
            self.status_label.configure(text=status_text)
            
    def set_status(
        self,
        status: Literal["pending", "processing", "success", "error", "cancelled"],
        message: str = ""
    ):
        """
        Set task status.
        
        Args:
            status: Status type
            message: Status message
        """
        icons = {
            "pending": "⏳",
            "processing": "⚙️",
            "success": "✓",
            "error": "✗",
            "cancelled": "⊘"
        }
        
        colors = {
            "pending": COLORS["text_muted"],
            "processing": COLORS["info"],
            "success": COLORS["success"],
            "error": COLORS["error"],
            "cancelled": COLORS["warning"]
        }
        
        self.status_icon.configure(text=icons.get(status, "⏳"))
        
        if message:
            self.status_label.configure(
                text=message,
                text_color=colors.get(status, COLORS["text_muted"])
            )
            
        # Hide cancel button if completed
        if status in ["success", "error", "cancelled"] and self.cancel_button:
            self.cancel_button.grid_remove()
            
        # Update progress bar color
        if status == "success":
            self.progress_bar.configure(progress_color=COLORS["success"])
            self.progress_bar.set(1.0)
        elif status == "error":
            self.progress_bar.configure(progress_color=COLORS["error"])
            
    def _on_cancel_clicked(self):
        """Handle cancel button click."""
        if self.on_cancel:
            self.on_cancel()
        self.set_status("cancelled", "Cancelled by user")
