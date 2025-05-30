# -*- coding: utf-8 -*-
"""
UI styling and theme management for the File Organizer application.
"""
import tkinter as tk
from tkinter import ttk
from config import UI_CONFIG


class UIStyles:
    """Manages UI styles and themes for the application."""

    def __init__(self, root):
        self.root = root
        self.style = ttk.Style()
        self.setup_styles()

    def setup_styles(self):
        """Configure TTK styles for the application."""
        # Try to set a base theme that allows more customization if possible
        # Common themes: 'clam', 'alt', 'default', 'classic'
        # 'clam' is usually good for customization
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            print("Theme 'clam' not available, using default theme.")

        # General style for all ttk widgets (if the theme allows)
        self.style.configure(
            ".",
            background=UI_CONFIG["theme"]["background_color"],
            foreground="black",  # Default text color
            font=(UI_CONFIG["theme"]["font_family"], UI_CONFIG["theme"]["font_size"]),
        )

        # Style for LabelFrame
        self.style.configure(
            "Custom.TLabelframe",
            background=UI_CONFIG["theme"]["background_color"],
            padding=UI_CONFIG["theme"]["padding"]["medium"],
        )
        self.style.configure(
            "Custom.TLabelframe.Label",  # Style for the label text of the LabelFrame
            background=UI_CONFIG["theme"]["background_color"],
            foreground="black",
            font=(
                UI_CONFIG["theme"]["font_family"],
                UI_CONFIG["theme"]["font_size"],
                "bold",
            ),
        )

        # Style for Buttons
        self.style.configure(
            "Custom.TButton",
            font=(
                UI_CONFIG["theme"]["font_family"],
                UI_CONFIG["theme"]["font_size"],
                "bold",
            ),
            padding=UI_CONFIG["theme"]["padding"]["medium"],
            background=UI_CONFIG["theme"]["primary_color"],
            foreground=UI_CONFIG["theme"]["text_color"],
            relief="raised",  # Border style
            borderwidth=2,
        )
        self.style.map(
            "Custom.TButton",
            background=[
                ("active", UI_CONFIG["theme"]["secondary_color"]),
                ("pressed", UI_CONFIG["theme"]["secondary_color"]),
            ],
            relief=[("pressed", "sunken")],
        )

        # Style for Progress Bar
        self.style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=UI_CONFIG["theme"]["background_color"],  # Channel color
            background=UI_CONFIG["theme"]["primary_color"],  # Bar color
            thickness=20,
        )

        # Style for Treeview
        self.style.configure(
            "Custom.Treeview",
            background=UI_CONFIG["theme"][
                "background_color"
            ],  # General widget background
            fieldbackground=UI_CONFIG["theme"]["background_color"],  # Cell background
            foreground="black",  # Text color
            font=(UI_CONFIG["theme"]["font_family"], UI_CONFIG["theme"]["font_size"]),
            rowheight=30,  # IMPROVEMENT: Increase row height
        )
        self.style.configure(
            "Custom.Treeview.Heading",
            font=(
                UI_CONFIG["theme"]["font_family"],
                UI_CONFIG["theme"]["font_size"] + 1,
                "bold",
            ),  # Slightly larger and bold
            background=UI_CONFIG["theme"]["primary_color"],
            foreground=UI_CONFIG["theme"]["text_color"],
            relief="raised",
        )
        self.style.map(
            "Custom.Treeview",
            background=[
                ("selected", UI_CONFIG["theme"]["primary_color"])
            ],  # IMPROVEMENT: Use config color
            foreground=[
                ("selected", UI_CONFIG["theme"]["text_color"])
            ],  # IMPROVEMENT: Use config color
        )


class LogManager:
    """Manages the activity log widget and its styling."""

    def __init__(self, log_text_widget):
        self.log_text = log_text_widget
        self.setup_log_styles()

    def setup_log_styles(self):
        """Configure log text colors based on message types."""
        self.log_text.tag_configure(
            "info", foreground=UI_CONFIG["theme"]["colors"].get("info_text", "black")
        )
        self.log_text.tag_configure(
            "error", foreground=UI_CONFIG["theme"]["colors"]["error"]
        )
        self.log_text.tag_configure(
            "success", foreground=UI_CONFIG["theme"]["colors"]["success"]
        )
        self.log_text.tag_configure(
            "warning", foreground=UI_CONFIG["theme"]["colors"]["warning"]
        )
