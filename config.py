#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration settings for the Timber Frame Construction application.
"""

# Default values for the application
DEFAULT_CONFIG = {
    "beam": {
        "width": 80,       # mm
        "height": 240,     # mm
        "spacing": 600,    # mm
        "color": "#8B4513"  # SaddleBrown
    },
    "top_board": {
        "thickness": 22,   # mm
        "color": "#DEB887"  # BurlyWood
    },
    "bottom_board": {
        "thickness": 22,   # mm
        "color": "#DEB887"  # BurlyWood
    },
    "element_names": {
        "beam": "Beam",
        "top_board": "Top Board",
        "bottom_board": "Bottom Board",
        "structure": "Floor Structure"
    }
}

# UI settings
UI_CONFIG = {
    "window": {
        "title": "Timber Frame Construction",
        "width": 900,
        "height": 600,
        "theme_color": "#4a7c59",  # Forest Green
    },
    "padding": {
        "default": 10,
        "large": 20,
    }
}