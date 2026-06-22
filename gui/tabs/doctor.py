"""Environment diagnostics tab."""
import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys
from gui.styles.theme import COLORS, FONTS, SIZES, SPACING
from gui.locales import DOCTOR


class DoctorTab(ctk.CTkFrame):
    """Tab for environment diagnostics (picx doctor)."""
    
    def __init__(self, master, app_instance, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.app = app_instance
        self.diagnostic_result = None
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Create UI
        self._create_header()
        self._create_action_section()
        self._create_result_section()
        
    def _create_header(self):
        """Create header section."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))
        
        # Title
        title = ctk.CTkLabel(
            header_frame,
            text=DOCTOR["title"],
            font=FONTS["subheading"],
            text_color=COLORS["text"]
        )
        title.pack(side="left")
        
        # Description
        desc_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=SIZES["corner_radius"])
        desc_frame.grid(row=1, column=0, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        description = DOCTOR["description"]
        desc_label = ctk.CTkLabel(
            desc_frame,
            text=description,
            font=FONTS["body"],
            text_color=COLORS["text_muted"],
            wraplength=500,
            justify="left"
        )
        desc_label.pack(padx=SIZES["padding"], pady=SIZES["padding"], anchor="w")
        
    def _create_action_section(self):
        """Create action buttons section."""
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=2, column=0, sticky="ew", padx=SIZES["padding"], pady=SIZES["padding_small"])
        
        # Run diagnostics button
        self.run_button = ctk.CTkButton(
            action_frame,
            text=DOCTOR["run_check"],
            height=SIZES["button_height"] + 10,
            command=self._run_diagnostics,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            font=FONTS["button"]
        )
        self.run_button.pack(side="left", padx=(0, SIZES["padding_small"]))
        
        # Copy button
        self.copy_button = ctk.CTkButton(
            action_frame,
            text=DOCTOR["copy_results"],
            height=SIZES["button_height"] + 10,
            command=self._copy_results,
            fg_color=COLORS["info"],
            hover_color="#1976D2",
            state="disabled"
        )
        self.copy_button.pack(side="left", padx=(0, SIZES["padding_small"]))
        
        # Refresh button
        refresh_button = ctk.CTkButton(
            action_frame,
            text=DOCTOR["refresh"],
            height=SIZES["button_height"] + 10,
            command=self._run_diagnostics,
            fg_color=COLORS["text_muted"],
            hover_color=COLORS["border"]
        )
        refresh_button.pack(side="left")
        
    def _create_result_section(self):
        """Create result display section."""
        self.result_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=SIZES["corner_radius"])
        self.result_frame.grid(row=3, column=0, sticky="nsew", padx=SIZES["padding"], pady=(SIZES["padding_small"], SIZES["padding"]))
        
        # Title
        title_frame = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=SIZES["padding"], pady=(SIZES["padding"], SIZES["padding_small"]))
        
        title = ctk.CTkLabel(
            title_frame,
            text=DOCTOR["diagnostic_results"],
            font=FONTS["subheading"],
            text_color=COLORS["text"]
        )
        title.pack(side="left")
        
        self.status_label = ctk.CTkLabel(
            title_frame,
            text=DOCTOR["click_to_start"],
            font=FONTS["small"],
            text_color=COLORS["text_muted"]
        )
        self.status_label.pack(side="right")
        
        # Results container
        self.results_container = ctk.CTkScrollableFrame(
            self.result_frame,
            fg_color="transparent"
        )
        self.results_container.pack(fill="both", expand=True, padx=SIZES["padding"], pady=(0, SIZES["padding"]))
        
        # Initial message
        self.initial_message = ctk.CTkLabel(
            self.results_container,
            text=DOCTOR["no_results"],
            font=FONTS["body"],
            text_color=COLORS["text_muted"]
        )
        self.initial_message.pack(pady=50)
        
    def _run_diagnostics(self):
        """Run environment diagnostics."""
        self.run_button.configure(state="disabled", text=DOCTOR["running"])
        self.app.update_status(DOCTOR["running_env_check"])
        
        # Clear previous results
        for widget in self.results_container.winfo_children():
            widget.destroy()
            
        # Show loading indicator
        loading_label = ctk.CTkLabel(
            self.results_container,
            text=DOCTOR["running_diagnostics"],
            font=FONTS["body"],
            text_color=COLORS["text_muted"]
        )
        loading_label.pack(pady=20)
        
        # Run diagnostics in background
        import threading
        
        def worker():
            try:
                # Try to import and run picx doctor
                result = self._run_picx_doctor()
                self.after(0, lambda: self._on_diagnostics_complete(result))
            except Exception as e:
                self.after(0, lambda: self._on_diagnostics_error(str(e)))
                
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        
    def _run_picx_doctor(self) -> dict:
        """Run picx doctor and parse results."""
        # First try to use picx Python API
        try:
            from picx import doctor
            report = doctor.collect_diagnostics()
            return {
                "success": True,
                "python_path": report.python_path,
                "picx_path": report.picx_path or "not found",
                "python_version": report.python_version,
                "pillow_version": report.pillow_version,
                "pyvips_status": report.pyvips_status,
                "libvips_version": report.libvips_version or "not available",
                "conda_environment": report.conda_environment or "not active",
                "homebrew_vips": report.homebrew_vips or "not found",
                "advice": report.advice or []
            }
        except ImportError:
            # Fallback to command line
            pass
        except Exception as e:
            return {"success": False, "error": f"picx API error: {str(e)}"}
            
        # Fallback: run picx doctor command
        try:
            result = subprocess.run(
                [sys.executable, "-m", "picx", "doctor"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": DOCTOR["timeout"]}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    def _on_diagnostics_complete(self, result):
        """Handle successful diagnostics."""
        self.run_button.configure(state="normal", text=DOCTOR["run_check"])
        self.app.update_status(DOCTOR["check_completed"])
        
        # Clear loading indicator
        for widget in self.results_container.winfo_children():
            widget.destroy()
            
        if result.get("success"):
            self._display_diagnostics(result)
            self.status_label.configure(text=DOCTOR["all_passed"], text_color=COLORS["success"])
            self.copy_button.configure(state="normal")
        else:
            error_msg = result.get("error", DOCTOR["unknown_error"])
            self._display_error(error_msg)
            self.status_label.configure(text=DOCTOR["some_failed"], text_color=COLORS["error"])
            
    def _display_diagnostics(self, result):
        """Display diagnostic results in a table format."""
        self.diagnostic_result = result
        
        # Create table
        checks = [
            ("Python", result.get("python_version", "N/A")),
            ("Python Path", result.get("python_path", "N/A")),
            ("picx", result.get("picx_path", "N/A")),
            ("Pillow", result.get("pillow_version", "N/A")),
            ("pyvips", result.get("pyvips_status", "N/A")),
            ("libvips", result.get("libvips_version", "N/A")),
            (DOCTOR["conda_env"], result.get("conda_environment", "N/A")),
            (DOCTOR["homebrew_vips"], result.get("homebrew_vips", "N/A")),
        ]
        
        # Header
        header_frame = ctk.CTkFrame(self.results_container, fg_color=COLORS["accent_tint"])
        header_frame.pack(fill="x", pady=(0, 2))
        
        check_header = ctk.CTkLabel(
            header_frame,
            text=DOCTOR["check"],
            font=FONTS["body_bold"],
            text_color=COLORS["text"],
            width=150,
            anchor="w"
        )
        check_header.pack(side="left", padx=10, pady=5)
        
        value_header = ctk.CTkLabel(
            header_frame,
            text=DOCTOR["value"],
            font=FONTS["body_bold"],
            text_color=COLORS["text"],
            anchor="w"
        )
        value_header.pack(side="left", fill="x", expand=True, padx=10, pady=5)
        
        # Rows
        for check_name, check_value in checks:
            row_frame = ctk.CTkFrame(self.results_container, fg_color=COLORS["surface_light"])
            row_frame.pack(fill="x", pady=1)
            
            name_label = ctk.CTkLabel(
                row_frame,
                text=check_name,
                font=FONTS["body_bold"],
                text_color=COLORS["text"],
                width=150,
                anchor="w"
            )
            name_label.pack(side="left", padx=10, pady=5)
            
            # Determine if value is good or warning
            if check_value in ["N/A", "not found", "not available", "not active"]:
                value_color = COLORS["warning"]
            elif "error" in str(check_value).lower() or "not" in str(check_value).lower():
                value_color = COLORS["warning"]
            else:
                value_color = COLORS["text"]
                
            value_label = ctk.CTkLabel(
                row_frame,
                text=str(check_value),
                font=FONTS["body"],
                text_color=value_color,
                anchor="w"
            )
            value_label.pack(side="left", fill="x", expand=True, padx=10, pady=5)
            
        # Display advice if available
        advice = result.get("advice", [])
        if advice:
            advice_frame = ctk.CTkFrame(self.results_container, fg_color=COLORS["warning"], corner_radius=4)
            advice_frame.pack(fill="x", pady=(10, 0))
            
            advice_title = ctk.CTkLabel(
                advice_frame,
                text=DOCTOR["advice_title"],
                font=FONTS["body_bold"],
                text_color=COLORS["text"],
                anchor="w"
            )
            advice_title.pack(fill="x", padx=10, pady=(5, 0))
            
            for item in advice:
                advice_item = ctk.CTkLabel(
                    advice_frame,
                    text=f"• {item}",
                    font=FONTS["body"],
                    text_color=COLORS["text"],
                    wraplength=500,
                    justify="left",
                    anchor="w"
                )
                advice_item.pack(fill="x", padx=10, pady=(0, 2))
                
            advice_frame.pack(pady=(10, 0))
            
    def _display_error(self, error_msg):
        """Display error message."""
        error_frame = ctk.CTkFrame(self.results_container, fg_color=COLORS["error"], corner_radius=4)
        error_frame.pack(fill="x", pady=10)
        
        error_label = ctk.CTkLabel(
            error_frame,
            text=f"Error: {error_msg}",
            font=FONTS["body"],
            text_color="white",
            wraplength=500,
            justify="left"
        )
        error_label.pack(padx=10, pady=10)
        
        # Add suggestions
        suggestions_frame = ctk.CTkFrame(self.results_container, fg_color=COLORS["surface_light"], corner_radius=4)
        suggestions_frame.pack(fill="x", pady=(0, 10))
        
        suggestions = [
            "Make sure picx is installed: pip install picx-image-optimizer",
            "Try running 'picx doctor' in command line",
            "Check that Python and pip are correctly configured"
        ]
        
        suggestions_label = ctk.CTkLabel(
            suggestions_frame,
            text="Troubleshooting:",
            font=FONTS["body_bold"],
            text_color=COLORS["text"],
            anchor="w"
        )
        suggestions_label.pack(fill="x", padx=10, pady=(5, 0))
        
        for suggestion in suggestions:
            suggestion_label = ctk.CTkLabel(
                suggestions_frame,
                text=f"• {suggestion}",
                font=FONTS["body"],
                text_color=COLORS["text_muted"],
                wraplength=500,
                justify="left",
                anchor="w"
            )
            suggestion_label.pack(fill="x", padx=10, pady=(0, 2))
            
        suggestions_frame.pack(pady=(0, 10))
        
    def _on_diagnostics_error(self, error_msg):
        """Handle diagnostics error."""
        self.run_button.configure(state="normal", text=DOCTOR["run_check"])
        self.app.update_status("Environment check failed")
        
        # Clear loading indicator
        for widget in self.results_container.winfo_children():
            widget.destroy()
            
        self._display_error(error_msg)
        self.status_label.configure(text="✗ Error occurred", text_color=COLORS["error"])
        
    def _copy_results(self):
        """Copy diagnostic results to clipboard."""
        if not self.diagnostic_result:
            return
            
        # Format results as text
        result = self.diagnostic_result
        text = "PicX Environment Diagnostics\n"
        text += "=" * 40 + "\n\n"
        
        checks = [
            ("Python", result.get("python_version", "N/A")),
            ("Python Path", result.get("python_path", "N/A")),
            ("picx", result.get("picx_path", "N/A")),
            ("Pillow", result.get("pillow_version", "N/A")),
            ("pyvips", result.get("pyvips_status", "N/A")),
            ("libvips", result.get("libvips_version", "N/A")),
            (DOCTOR["conda_env"], result.get("conda_environment", "N/A")),
            (DOCTOR["homebrew_vips"], result.get("homebrew_vips", "N/A")),
        ]
        
        for check_name, check_value in checks:
            text += f"{check_name}: {check_value}\n"
            
        advice = result.get("advice", [])
        if advice:
            text += f"\n{DOCTOR['advice_title']}\n"
            for item in advice:
                text += f"  • {item}\n"
                
        # Copy to clipboard
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()
        
        messagebox.showinfo(DOCTOR["copy_success"], DOCTOR["results_copied"])
