#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main application window for the Timber Frame Construction application.
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

from models.floor_structure_config import FloorStructureConfig, BeamConfig
from viewmodel.floor_viewmodel import FloorViewModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'components')))

from config import UI_CONFIG
from controllers.floor_controller import FloorController
from ui.components.beam_config import BeamConfigFrame
from ui.components.board_config import BoardConfigFrame
from ui.components.color_picker import ColorPickerFrame


class TimberFrameApp:

    def __init__(self, root, controller: FloorController):

        self.root = root
        self.view_model = FloorViewModel(controller)

        self._setup_window()
        self._create_styles()
        self._create_menu()
        self._create_main_frame()
        self._create_status_bar()

    def _setup_window(self):
        """Set up the main application window."""
        window_config = UI_CONFIG["window"]
        self.root.title(window_config["title"])
        self.root.geometry(f"{window_config['width']}x{window_config['height']}")
        self.root.minsize(800, 500)

        # Center the window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = int((screen_width - window_config["width"]) / 2)
        y_position = int((screen_height - window_config["height"]) / 2)
        self.root.geometry(f"+{x_position}+{y_position}")

    def _create_styles(self):
        """Create ttk styles for the application."""
        self.style = ttk.Style()

        # Use the main theme color
        theme_color = UI_CONFIG["window"]["theme_color"]
        self._configure_styles_for_widgets(theme_color)

    def _configure_styles_for_widgets(self, theme_color):
        self.style.configure("TFrame", background="#f8f9fa")
        self.style.configure("TLabel", background="#f8f9fa", font=("Helvetica", 10))
        self.style.configure("TButton", font=("Helvetica", 10))
        self.style.configure("Primary.TButton", background=theme_color, foreground="white")
        self.style.configure("Header.TLabel", font=("Helvetica", 12, "bold"))
        self.style.configure("Title.TLabel", font=("Helvetica", 14, "bold"))

    def _create_menu(self):
        """Create the application menu."""
        self.menu_bar = tk.Menu(self.root)

        self._create_file_menu()
        self._create_help_menu()

        self.root.config(menu=self.menu_bar)

    def _create_help_menu(self):
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Documentation", command=self._show_documentation)
        help_menu.add_command(label="About", command=self._show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def _create_file_menu(self):
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Import from CAD", command=lambda: print("Import from CAD"))
        file_menu.add_command(label="Export to CAD", command=lambda: print("Export to CAD"))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_main_frame(self):
        """Create the main frame with configuration panels."""
        padding = UI_CONFIG["padding"]["default"]

        # Main container frame with padding around the edges
        self.main_frame = ttk.Frame(self.root, padding=padding)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=padding, pady=padding)

        self._create_title_label_main_frame(padding)

        # Create a notebook for tabbed interface
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Configuration tab
        self.config_tab = ttk.Frame(self.notebook, padding=padding)
        self.notebook.add(self.config_tab, text="Configuration")

        # Create left and right panes in configuration tab
        left_frame = ttk.Frame(self.config_tab)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, padding))

        right_frame = ttk.Frame(self.config_tab)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(padding, 0))

        # Beam configuration in left frame
        self.beam_config = BeamConfigFrame(left_frame)
        self.beam_config.pack(fill=tk.BOTH, expand=True)

        # Board configuration in right frame
        self.board_config = BoardConfigFrame(right_frame)
        self.board_config.pack(fill=tk.BOTH, expand=True)

        # Color picker tab
        self.color_tab = ttk.Frame(self.notebook, padding=padding)
        self.notebook.add(self.color_tab, text="Colors & Names")

        self.color_picker = ColorPickerFrame(self.color_tab)
        self.color_picker.pack(fill=tk.BOTH, expand=True)

        # Button frame at the bottom
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=(padding, 0))

        # Create and export buttons
        self.create_button = ttk.Button(
            button_frame,
            text="Create Structure",
            command=self._create_structure,
            style="Primary.TButton"
        )
        self.create_button.pack(side=tk.RIGHT, padx=(padding, 0))

        self.export_button = ttk.Button(
            button_frame,
            text="Create",
            command=self._on_create_structure,
        )
        self.export_button.pack(side=tk.RIGHT, padx=(padding, 0))

        self.import_button = ttk.Button(
            button_frame,
            text="Import from CAD",
            command=lambda: print("Import from CAD")
        )
        self.import_button.pack(side=tk.RIGHT)

    def _create_title_label_main_frame(self, padding):
        title_label = ttk.Label(
            self.main_frame,
            text="Timber Frame Floor Generator",
            style="Title.TLabel"
        )
        title_label.pack(fill=tk.X, pady=(0, padding * 2))

    def _create_status_bar(self):
        """Create a status bar at the bottom of the window."""
        self.status_bar = ttk.Label(
            self.root,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(10, 2)
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def _create_structure(self):
        pass

    def _on_create_structure(self):

        spacing = self.beam_config.get_values()["spacing"]
        beam_config = self._setup_beam_config()
        structure_config = FloorStructureConfig(spacing=spacing,
                                                beam_config=beam_config)

        self.view_model.set_config(structure_config)
        result = self.view_model.create_structure()
        if result:
            self._set_status("Structure created successfully.")
        else:
            self._set_status("Failed to create structure.")

    def _setup_beam_config(self):
        beam_height = self.beam_config.get_values()["height"]
        beam_width = self.beam_config.get_values()["width"]
        beam_color = self.color_picker.get_values()["beam_color"]
        beam_name = self.color_picker.get_values()["beam_name"]
        return BeamConfig(height=beam_height, width=beam_width,
                          color=beam_color,
                          name=beam_name)

    @staticmethod
    def _show_documentation():
        """Show application documentation."""
        messagebox.showinfo(
            "Documentation",
            "Timber Frame Construction Application\n\n"
            "This application allows you to create timber frame floor structures "
            "with configurable beam dimensions and board thicknesses.\n\n"
            "1. Import a floor element from CAD software\n"
            "2. Configure beam dimensions and spacing\n"
            "3. Configure top and bottom board thicknesses\n"
            "4. Set element names and colors\n"
            "5. Create the structure\n"
            "6. Export the structure back to CAD software"
        )

    @staticmethod
    def _show_about():
        """Show information about the application."""
        messagebox.showinfo(
            "About",
            "Timber Frame Construction Application\n"
            "Version 1.0\n\n"
            "Created as a teaching tool for timber frame construction.\n"
            "© 2025"
        )

    def _set_status(self, message):
        """Set the status bar message."""
        self.status_bar.config(text=message)
