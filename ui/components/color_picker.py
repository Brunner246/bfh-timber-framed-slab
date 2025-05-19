#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Color picker and name configuration component.
"""
import tkinter as tk
from tkinter import ttk, colorchooser
import sys
import os

# Add the project root to the path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config import DEFAULT_CONFIG, UI_CONFIG


class ColorPickerFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=UI_CONFIG["padding"]["default"])

        self.beam_defaults = DEFAULT_CONFIG["beam"]
        self.top_board_defaults = DEFAULT_CONFIG["top_board"]
        self.bottom_board_defaults = DEFAULT_CONFIG["bottom_board"]
        self.element_names = DEFAULT_CONFIG["element_names"]

        self._create_widgets()
    
    def _create_widgets(self):
        padding = UI_CONFIG["padding"]["default"]

        # Titles for sections
        ttk.Label(self, text="Element Names", style="Header.TLabel").grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, padding)
        )
        
        ttk.Label(self, text="Element Colors", style="Header.TLabel").grid(
            row=0, column=2, columnspan=2, sticky=tk.W, pady=(0, padding)
        )
        
        # Structure name
        ttk.Label(self, text="Structure Name:").grid(row=1, column=0, sticky=tk.W, pady=(0, padding))
        
        self.structure_name_var = tk.StringVar(value=self.element_names["structure"])
        self.structure_name_entry = ttk.Entry(self, textvariable=self.structure_name_var, width=20)
        self.structure_name_entry.grid(row=1, column=1, sticky=tk.W, pady=(0, padding))
        
        # Beam name
        ttk.Label(self, text="Beam Name:").grid(row=2, column=0, sticky=tk.W, pady=(0, padding))
        
        self.beam_name_var = tk.StringVar(value=self.element_names["beam"])
        self.beam_name_entry = ttk.Entry(self, textvariable=self.beam_name_var, width=20)
        self.beam_name_entry.grid(row=2, column=1, sticky=tk.W, pady=(0, padding))
        
        # Top board name
        ttk.Label(self, text="Top Board Name:").grid(row=3, column=0, sticky=tk.W, pady=(0, padding))
        
        self.top_board_name_var = tk.StringVar(value=self.element_names["top_board"])
        self.top_board_name_entry = ttk.Entry(self, textvariable=self.top_board_name_var, width=20)
        self.top_board_name_entry.grid(row=3, column=1, sticky=tk.W, pady=(0, padding))
        
        # Bottom board name
        ttk.Label(self, text="Bottom Board Name:").grid(row=4, column=0, sticky=tk.W, pady=(0, padding))
        
        self.bottom_board_name_var = tk.StringVar(value=self.element_names["bottom_board"])
        self.bottom_board_name_entry = ttk.Entry(self, textvariable=self.bottom_board_name_var, width=20)
        self.bottom_board_name_entry.grid(row=4, column=1, sticky=tk.W, pady=(0, padding))
        
        # Beam color
        ttk.Label(self, text="Beam Color:").grid(row=2, column=2, sticky=tk.W, pady=(0, padding))
        
        self.beam_color_var = tk.StringVar(value=self._cw_color_nr_to_rgb(self.beam_defaults["color"]))
        self.beam_color_frame = tk.Frame(self, width=30, height=20, bg=self.beam_color_var.get())
        self.beam_color_frame.grid(row=2, column=3, sticky=tk.W, pady=(0, padding), padx=(0, padding))
        
        self.beam_color_button = ttk.Button(
            self,
            text="Choose...",
            command=lambda: self._choose_color(self.beam_color_var, self.beam_color_frame)
        )
        self.beam_color_button.grid(row=2, column=4, sticky=tk.W, pady=(0, padding))
        
        # Top board color
        ttk.Label(self, text="Top Board Color:").grid(row=3, column=2, sticky=tk.W, pady=(0, padding))
        
        self.top_board_color_var = tk.StringVar(value=self._cw_color_nr_to_rgb(self.top_board_defaults["color"]))
        self.top_board_color_frame = tk.Frame(
            self, width=30, height=20, bg=self.top_board_color_var.get()
        )
        self.top_board_color_frame.grid(row=3, column=3, sticky=tk.W, pady=(0, padding), padx=(0, padding))
        
        self.top_board_color_button = ttk.Button(
            self,
            text="Choose...",
            command=lambda: self._choose_color(self.top_board_color_var, self.top_board_color_frame)
        )
        self.top_board_color_button.grid(row=3, column=4, sticky=tk.W, pady=(0, padding))
        
        # Bottom board color
        ttk.Label(self, text="Bottom Board Color:").grid(row=4, column=2, sticky=tk.W, pady=(0, padding))
        
        self.bottom_board_color_var = tk.StringVar(value=self._cw_color_nr_to_rgb(self.bottom_board_defaults["color"]))
        self.bottom_board_color_frame = tk.Frame(
            self, width=30, height=20, bg=self.bottom_board_color_var.get()
        )
        self.bottom_board_color_frame.grid(row=4, column=3, sticky=tk.W, pady=(0, padding), padx=(0, padding))
        
        self.bottom_board_color_button = ttk.Button(
            self,
            text="Choose...",
            command=lambda: self._choose_color(self.bottom_board_color_var, self.bottom_board_color_frame)
        )
        self.bottom_board_color_button.grid(row=4, column=4, sticky=tk.W, pady=(0, padding))

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.columnconfigure(3, weight=0)
        self.columnconfigure(4, weight=1)
    
    @staticmethod
    def _choose_color(color_var, color_frame):
        import utility_controller
        import visualization_controller
        import cadwork

        color_nr = utility_controller.get_user_color(1)
        hex_color = ColorPickerFrame._cw_color_nr_to_rgb(color_nr)

        color_var.set(color_nr) #f"{rgb_color.r}, {rgb_color.g}, {rgb_color.b}"

        color_frame.config(bg=hex_color)

    @staticmethod
    def _cw_color_nr_to_rgb(color_nr):
        import visualization_controller
        import cadwork
        rgb_color = visualization_controller.get_rgb_from_cadwork_color_id(color_nr)
        hex_color = f"#{rgb_color.r:02x}{rgb_color.g:02x}{rgb_color.b:02x}"
        return hex_color

    def get_values(self):

        return {
            "beam_color": int(self.beam_color_var.get()),
            "top_board_color": self.top_board_color_var.get(),
            "bottom_board_color": self.bottom_board_color_var.get(),
            "structure_name": self.structure_name_var.get(),
            "beam_name": self.beam_name_var.get(),
            "top_board_name": self.top_board_name_var.get(),
            "bottom_board_name": self.bottom_board_name_var.get()
        }
    
    def set_values(self, beam_color, top_board_color, bottom_board_color,
                 structure_name, beam_name, top_board_name, bottom_board_name):
        self.beam_color_var.set(beam_color)
        self.beam_color_frame.config(bg=beam_color)
        
        self.top_board_color_var.set(top_board_color)
        self.top_board_color_frame.config(bg=top_board_color)
        
        self.bottom_board_color_var.set(bottom_board_color)
        self.bottom_board_color_frame.config(bg=bottom_board_color)
        
        self.structure_name_var.set(structure_name)
        self.beam_name_var.set(beam_name)
        self.top_board_name_var.set(top_board_name)
        self.bottom_board_name_var.set(bottom_board_name)