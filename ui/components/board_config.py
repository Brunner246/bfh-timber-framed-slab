import tkinter as tk
from tkinter import ttk
import sys
import os

from config import DEFAULT_CONFIG, UI_CONFIG


class BoardConfigFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Board Configuration", padding=UI_CONFIG["padding"]["default"])

        self.top_board_defaults = DEFAULT_CONFIG["top_board"]
        self.bottom_board_defaults = DEFAULT_CONFIG["bottom_board"]

        self.top_thickness_var = None
        self.bottom_thickness_var = None

        self._create_widgets()
    
    def _create_widgets(self):
        padding = UI_CONFIG["padding"]["default"]

        ttk.Label(self, text="Top Board Thickness (mm):").grid(row=0, column=0, sticky=tk.W, pady=(0, padding))

        self._create_top_plate_widget(padding)
        self._create_bottom_plate_widget(padding)
        self._crate_description_widget(padding)

        # Allow the columns to expand
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def _crate_description_widget(self, padding):
        description = (
            "Boards represent the top and bottom planking of the floor structure. "
            "The boards follow the exact perimeter of the imported floor element."
        )
        description_label = ttk.Label(
            self,
            text=description,
            wraplength=300,
            justify=tk.LEFT
        )
        description_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(padding, 0))

    def _create_bottom_plate_widget(self, padding):
        self.bottom_thickness_var = tk.DoubleVar(value=self.bottom_board_defaults["thickness"])
        self.bottom_thickness_spinbox = ttk.Spinbox(
            self,
            from_=10.0,
            to=50.0,
            increment=1.0,
            textvariable=self.bottom_thickness_var,
            width=10
        )
        self.bottom_thickness_spinbox.grid(row=1, column=1, sticky=tk.W, pady=(0, padding))

    def _create_top_plate_widget(self, padding):
        self.top_thickness_var = tk.DoubleVar(value=self.top_board_defaults["thickness"])
        self.top_thickness_spinbox = ttk.Spinbox(
            self,
            from_=10.0,
            to=50.0,
            increment=1.0,
            textvariable=self.top_thickness_var,
            width=10
        )
        self.top_thickness_spinbox.grid(row=0, column=1, sticky=tk.W, pady=(0, padding))
        ttk.Label(self, text="Bottom Board Thickness (mm):").grid(row=1, column=0, sticky=tk.W, pady=(0, padding))

    def get_values(self):
        return {
            "top_thickness": self.top_thickness_var.get(),
            "bottom_thickness": self.bottom_thickness_var.get()
        }
    
    def set_values(self, top_thickness, bottom_thickness):
        self.top_thickness_var.set(top_thickness)
        self.bottom_thickness_var.set(bottom_thickness)