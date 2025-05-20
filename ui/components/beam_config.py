import tkinter as tk
from tkinter import ttk

from config import DEFAULT_CONFIG, UI_CONFIG


class BeamConfigFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Beam Configuration", padding=UI_CONFIG["padding"]["default"])

        # Get default values from configuration
        self.beam_defaults = DEFAULT_CONFIG["beam"]

        # Create input fields
        self._create_widgets()

    def _create_widgets(self):
        """Create the input widgets for beam configuration."""
        padding = UI_CONFIG["padding"]["default"]

        self._create_beam_width_widget(padding)
        self._create_beam_height_widget(padding)
        self._create_beam_spacing_widget(padding)
        self._create_description_widget(padding)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def _create_description_widget(self, padding):
        description = (
            "Beams...."
        )
        description_label = ttk.Label(
            self,
            text=description,
            wraplength=300,
            justify=tk.LEFT
        )
        description_label.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(padding, 0))

    def _create_beam_spacing_widget(self, padding):
        ttk.Label(self, text="Beam Spacing (mm):").grid(row=2, column=0, sticky=tk.W, pady=(0, padding))
        self.beam_spacing_var = tk.DoubleVar(value=self.beam_defaults["spacing"])
        self.beam_spacing_spinbox = ttk.Spinbox(
            self,
            from_=300.0,
            to=1200.0,
            increment=50.0,
            textvariable=self.beam_spacing_var,
            width=10
        )
        self.beam_spacing_spinbox.grid(row=2, column=1, sticky=tk.W, pady=(0, padding))

    def _create_beam_height_widget(self, padding):
        ttk.Label(self, text="Beam Height (mm):").grid(row=1, column=0, sticky=tk.W, pady=(0, padding))
        self.beam_height_var = tk.DoubleVar(value=self.beam_defaults["height"])
        self.beam_height_spinbox = ttk.Spinbox(
            self,
            from_=100.0,
            to=500.0,
            increment=10.0,
            textvariable=self.beam_height_var,
            width=10
        )
        self.beam_height_spinbox.grid(row=1, column=1, sticky=tk.W, pady=(0, padding))

    def _create_beam_width_widget(self, padding):
        ttk.Label(self, text="Beam Width (mm):").grid(row=0, column=0, sticky=tk.W, pady=(0, padding))
        self.beam_width_var = tk.DoubleVar(value=self.beam_defaults["width"])
        self.beam_width_spinbox = ttk.Spinbox(
            self,
            from_=40.0,
            to=200.0,
            increment=5.0,
            textvariable=self.beam_width_var,
            width=10
        )
        self.beam_width_spinbox.grid(row=0, column=1, sticky=tk.W, pady=(0, padding))

    def get_values(self):
        return {
            "width": self.beam_width_var.get(),
            "height": self.beam_height_var.get(),
            "spacing": self.beam_spacing_var.get()
        }

    def set_values(self, width, height, spacing):
        self.beam_width_var.set(width)
        self.beam_height_var.set(height)
        self.beam_spacing_var.set(spacing)
