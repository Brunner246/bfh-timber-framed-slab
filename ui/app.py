import os
import sys
import tkinter as tk
from tkinter import ttk

from models.floor_structure_config import FloorStructureConfig, BeamConfig, PanelConfig
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

        theme_color = UI_CONFIG["window"]["theme_color"]
        self._configure_styles_for_widgets(theme_color)

    def _configure_styles_for_widgets(self, theme_color):
        self.style.configure("TFrame", background="#f8f9fa")
        self.style.configure("TLabel", background="#f8f9fa", font=("Helvetica", 10))
        self.style.configure("TButton", font=("Helvetica", 10))
        self.style.configure("Primary.TButton", background=theme_color, foreground="white")
        self.style.configure("Header.TLabel", font=("Helvetica", 12, "bold"))
        self.style.configure("Title.TLabel", font=("Helvetica", 14, "bold"))

    def _create_main_frame(self):
        """Create the main frame with configuration panels."""
        padding = UI_CONFIG["padding"]["default"]

        # Main container frame with padding around the edges
        self.main_frame = ttk.Frame(self.root, padding=padding)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=padding, pady=padding)

        self._create_title_label_main_frame(padding)

        self._setup_notebook_tabbed_interface()
        self._setup_configuration_tab(padding)
        left_frame = self._setup_left_and_right_panes_in_config_tab(padding)

        right_frame = self._setup_right_frame(padding)

        self._setup_beam_config_in_left_frame(left_frame)
        self._setup_beam_config_in_right_frame(right_frame)

        self._setup_color_picker_tab(padding)
        self._setup_color_picker()

        self._setup_buttons(padding)

    def _setup_buttons(self, padding):
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=(padding, 0))
        self.export_button = ttk.Button(
            button_frame,
            text="Create",
            command=self._on_create_structure,
        )
        self.export_button.pack(side=tk.RIGHT, padx=(padding, 0))

    def _setup_color_picker(self):
        self.color_picker = ColorPickerFrame(self.color_tab)
        self.color_picker.pack(fill=tk.BOTH, expand=True)

    def _setup_color_picker_tab(self, padding):
        self.color_tab = ttk.Frame(self.notebook, padding=padding)
        self.notebook.add(self.color_tab, text="Colors & Names")

    def _setup_beam_config_in_right_frame(self, right_frame):
        self.board_config = BoardConfigFrame(right_frame)
        self.board_config.pack(fill=tk.BOTH, expand=True)

    def _setup_beam_config_in_left_frame(self, left_frame):
        self.beam_config = BeamConfigFrame(left_frame)
        self.beam_config.pack(fill=tk.BOTH, expand=True)

    def _setup_right_frame(self, padding):
        right_frame = ttk.Frame(self.config_tab)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(padding, 0))
        return right_frame

    def _setup_left_and_right_panes_in_config_tab(self, padding):
        left_frame = ttk.Frame(self.config_tab)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, padding))
        return left_frame

    def _setup_configuration_tab(self, padding):
        self.config_tab = ttk.Frame(self.notebook, padding=padding)
        self.notebook.add(self.config_tab, text="Configuration")

    def _setup_notebook_tabbed_interface(self):
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

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

    def _on_create_structure(self):

        spacing = self.beam_config.get_values()["spacing"]
        beam_config = self._setup_beam_config()
        top_panel_config = self._setup_top_panel_config()
        bottom_panel_config = self._setup_bottom_panel_config()
        structure_config = FloorStructureConfig(spacing=spacing,
                                                name=self.color_picker.get_values()["structure_name"],
                                                beam_config=beam_config,
                                                top_panel_config=top_panel_config,
                                                bottom_panel_config=bottom_panel_config)

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

    def _setup_top_panel_config(self):
        panel_thickness = self.board_config.get_values()["top_thickness"]
        panel_color = self.color_picker.get_values()["top_board_color"]
        panel_name = self.color_picker.get_values()["top_board_name"]

        return PanelConfig(thickness=panel_thickness,
                           color=panel_color,
                           name=panel_name)

    def _setup_bottom_panel_config(self):
        panel_thickness = self.board_config.get_values()["bottom_thickness"]
        panel_color = self.color_picker.get_values()["bottom_board_color"]
        panel_name = self.color_picker.get_values()["bottom_board_name"]

        return PanelConfig(thickness=panel_thickness,
                           color=panel_color,
                           name=panel_name)

    def _set_status(self, message):
        """Set the status bar message."""
        self.status_bar.config(text=message)
