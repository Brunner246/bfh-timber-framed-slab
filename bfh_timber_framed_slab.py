#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Timber Frame Construction Application
-------------------------------------
Main entry point for the Timber Frame Construction application.

This application allows for the design of timber frame structures
with configurable beam dimensions and board thicknesses.
Students will implement the CAD API integration.
"""
import os
import sys
import tkinter as tk

project_root = os.path.abspath(os.path.dirname(__file__))
ui_dir = os.path.join(project_root, 'ui')
ui_components_dir = os.path.join(ui_dir, 'components')
controller_dir = os.path.join(project_root, 'controllers')

paths = [project_root, ui_dir, ui_components_dir, controller_dir]

[sys.path.append(path) for path in paths if path not in sys.path]

print("\n".join(sys.path))

from ui.app import TimberFrameApp
from controllers.floor_controller import FloorController


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    controller = FloorController()
    app = TimberFrameApp(root, controller)
    root.mainloop()


if __name__ == "__main__":
    main()
