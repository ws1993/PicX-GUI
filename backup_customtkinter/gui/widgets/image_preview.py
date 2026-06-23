"""Image preview widget."""
import customtkinter as ctk
from PIL import Image, ImageTk
from typing import Optional, Tuple
from gui.styles.theme import COLORS, FONTS, SIZES, SPACING


class ImagePreview(ctk.CTkFrame):
    """Widget for previewing images with zoom and comparison."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["surface"], corner_radius=SIZES["corner_radius"], **kwargs)
        
        self.original_image = None
        self.processed_image = None
        self.display_image = None
        self.zoom_level = 1.0
        self.pan_x = 0
        self.pan_y = 0
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create UI
        self._create_toolbar()
        self._create_canvas()
        self._create_info_bar()
        
    def _create_toolbar(self):
        """Create toolbar with zoom controls."""
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="ew", padx=SIZES["padding_small"], pady=(SIZES["padding_small"], 0))
        
        # Zoom controls
        zoom_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        zoom_frame.pack(side="left")
        
        zoom_out_btn = ctk.CTkButton(
            zoom_frame,
            text="-",
            width=30,
            height=30,
            command=self._zoom_out,
            fg_color=COLORS["text_muted"],
            hover_color=COLORS["border"]
        )
        zoom_out_btn.pack(side="left", padx=2)
        
        self.zoom_label = ctk.CTkLabel(
            zoom_frame,
            text="100%",
            font=FONTS["small"],
            width=50
        )
        self.zoom_label.pack(side="left", padx=5)
        
        zoom_in_btn = ctk.CTkButton(
            zoom_frame,
            text="+",
            width=30,
            height=30,
            command=self._zoom_in,
            fg_color=COLORS["text_muted"],
            hover_color=COLORS["border"]
        )
        zoom_in_btn.pack(side="left", padx=2)
        
        zoom_fit_btn = ctk.CTkButton(
            zoom_frame,
            text="Fit",
            width=40,
            height=30,
            command=self._zoom_fit,
            fg_color=COLORS["info"],
            hover_color="#1976D2"
        )
        zoom_fit_btn.pack(side="left", padx=5)
        
        zoom_100_btn = ctk.CTkButton(
            zoom_frame,
            text="1:1",
            width=40,
            height=30,
            command=self._zoom_100,
            fg_color=COLORS["info"],
            hover_color="#1976D2"
        )
        zoom_100_btn.pack(side="left", padx=2)
        
        # View mode buttons
        view_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        view_frame.pack(side="right")
        
        self.view_mode = ctk.StringVar(value="single")
        
        single_btn = ctk.CTkRadioButton(
            view_frame,
            text="Single",
            variable=self.view_mode,
            value="single",
            command=self._on_view_mode_changed
        )
        single_btn.pack(side="left", padx=5)
        
        compare_btn = ctk.CTkRadioButton(
            view_frame,
            text="Compare",
            variable=self.view_mode,
            value="compare",
            command=self._on_view_mode_changed
        )
        compare_btn.pack(side="left", padx=5)
        
    def _create_canvas(self):
        """Create image canvas."""
        canvas_frame = ctk.CTkFrame(self, fg_color=COLORS["dark_block"], corner_radius=4)
        canvas_frame.grid(row=1, column=0, sticky="nsew", padx=SIZES["padding_small"], pady=SIZES["padding_small"])
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_rowconfigure(0, weight=1)
        
        # Canvas for image display
        self.canvas = ctk.CTkCanvas(
            canvas_frame,
            bg=COLORS["dark_block"],
            highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Bind mouse events
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<ButtonPress-1>", self._on_button_press)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_button_release)
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        
    def _create_info_bar(self):
        """Create image info bar."""
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.grid(row=2, column=0, sticky="ew", padx=SIZES["padding_small"], pady=(0, SIZES["padding_small"]))
        
        self.info_label = ctk.CTkLabel(
            self.info_frame,
            text="No image loaded",
            font=FONTS["small"],
            text_color=COLORS["text_muted"]
        )
        self.info_label.pack(side="left")
        
    def load_image(self, image_path: str):
        """
        Load an image for preview.
        
        Args:
            image_path: Path to the image file
        """
        try:
            self.original_image = Image.open(image_path)
            self.processed_image = None
            self._update_display()
            self._update_info()
        except Exception as e:
            print(f"Error loading image: {e}")
            
    def load_images(self, original_path: str, processed_path: str):
        """
        Load original and processed images for comparison.
        
        Args:
            original_path: Path to the original image
            processed_path: Path to the processed image
        """
        try:
            self.original_image = Image.open(original_path)
            self.processed_image = Image.open(processed_path)
            self._update_display()
            self._update_info()
        except Exception as e:
            print(f"Error loading images: {e}")
            
    def _update_display(self):
        """Update the canvas display."""
        if not self.original_image:
            return
            
        # Get canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            return
            
        # Determine which image to show
        if self.view_mode.get() == "single" or not self.processed_image:
            image = self.original_image
        else:
            # Compare mode - show side by side
            self._show_comparison()
            return
            
        # Resize image based on zoom
        img_width, img_height = image.size
        display_width = int(img_width * self.zoom_level)
        display_height = int(img_height * self.zoom_level)
        
        # Resize image
        if self.zoom_level != 1.0:
            display_image = image.resize((display_width, display_height), Image.Resampling.LANCZOS)
        else:
            display_image = image
            
        # Convert to PhotoImage
        self.display_image = ImageTk.PhotoImage(display_image)
        
        # Clear canvas and draw image
        self.canvas.delete("all")
        
        # Center image with pan offset
        x = (canvas_width - display_width) // 2 + self.pan_x
        y = (canvas_height - display_height) // 2 + self.pan_y
        
        self.canvas.create_image(x, y, anchor="nw", image=self.display_image)
        
        # Update zoom label
        self.zoom_label.configure(text=f"{int(self.zoom_level * 100)}%")
        
    def _show_comparison(self):
        """Show side-by-side comparison."""
        if not self.original_image or not self.processed_image:
            return
            
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Calculate size for each image (half width)
        half_width = canvas_width // 2 - 10
        
        # Resize images to fit
        orig_width, orig_height = self.original_image.size
        proc_width, proc_height = self.processed_image.size
        
        # Calculate scale for each image
        orig_scale = min(half_width / orig_width, canvas_height / orig_height)
        proc_scale = min(half_width / proc_width, canvas_height / proc_height)
        
        scale = min(orig_scale, proc_scale) * self.zoom_level
        
        # Resize images
        new_orig_size = (int(orig_width * scale), int(orig_height * scale))
        new_proc_size = (int(proc_width * scale), int(proc_height * scale))
        
        orig_display = self.original_image.resize(new_orig_size, Image.Resampling.LANCZOS)
        proc_display = self.processed_image.resize(new_proc_size, Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        self.orig_photo = ImageTk.PhotoImage(orig_display)
        self.proc_photo = ImageTk.PhotoImage(proc_display)
        
        # Clear canvas
        self.canvas.delete("all")
        
        # Draw images side by side
        y = (canvas_height - new_orig_size[1]) // 2
        
        # Original on left
        x1 = half_width // 2 - new_orig_size[0] // 2
        self.canvas.create_image(x1, y, anchor="nw", image=self.orig_photo)
        
        # Processed on right
        x2 = half_width + 10 + half_width // 2 - new_proc_size[0] // 2
        self.canvas.create_image(x2, y, anchor="nw", image=self.proc_photo)
        
        # Add labels
        self.canvas.create_text(x1 + new_orig_size[0] // 2, y - 10, 
                               text="Original", fill="white", font=("Arial", 10))
        self.canvas.create_text(x2 + new_proc_size[0] // 2, y - 10, 
                               text="Processed", fill="white", font=("Arial", 10))
        
        # Add divider line
        self.canvas.create_line(half_width + 5, 0, half_width + 5, canvas_height, 
                               fill="white", width=2)
        
    def _update_info(self):
        """Update image info display."""
        if not self.original_image:
            self.info_label.configure(text="No image loaded")
            return
            
        orig_width, orig_height = self.original_image.size
        info_text = f"Original: {orig_width}x{orig_height}"
        
        if self.processed_image:
            proc_width, proc_height = self.processed_image.size
            info_text += f" | Processed: {proc_width}x{proc_height}"
            
        self.info_label.configure(text=info_text)
        
    def _zoom_in(self):
        """Zoom in."""
        self.zoom_level = min(self.zoom_level * 1.2, 5.0)
        self._update_display()
        
    def _zoom_out(self):
        """Zoom out."""
        self.zoom_level = max(self.zoom_level / 1.2, 0.1)
        self._update_display()
        
    def _zoom_fit(self):
        """Zoom to fit."""
        if not self.original_image:
            return
            
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        img_width, img_height = self.original_image.size
        
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        
        self.zoom_level = min(scale_x, scale_y) * 0.9  # 90% to add some padding
        self.pan_x = 0
        self.pan_y = 0
        self._update_display()
        
    def _zoom_100(self):
        """Zoom to 100%."""
        self.zoom_level = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self._update_display()
        
    def _on_mousewheel(self, event):
        """Handle mouse wheel for zoom."""
        if event.delta > 0:
            self._zoom_in()
        else:
            self._zoom_out()
            
    def _on_button_press(self, event):
        """Handle button press for pan."""
        self._drag_start_x = event.x
        self._drag_start_y = event.y
        
    def _on_mouse_drag(self, event):
        """Handle mouse drag for pan."""
        dx = event.x - self._drag_start_x
        dy = event.y - self._drag_start_y
        
        self.pan_x += dx
        self.pan_y += dy
        
        self._drag_start_x = event.x
        self._drag_start_y = event.y
        
        self._update_display()
        
    def _on_button_release(self, event):
        """Handle button release."""
        pass
        
    def _on_canvas_resize(self, event):
        """Handle canvas resize."""
        self._update_display()
        
    def _on_view_mode_changed(self):
        """Handle view mode change."""
        self._update_display()
        
    def clear(self):
        """Clear the preview."""
        self.original_image = None
        self.processed_image = None
        self.display_image = None
        self.canvas.delete("all")
        self.info_label.configure(text="No image loaded")
