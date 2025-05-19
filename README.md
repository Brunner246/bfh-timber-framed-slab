# Timber Frame Construction Application

A Python application for creating timber frame floor structures with configurable beam dimensions and board thicknesses.

## Overview

This application provides a "modern Tkinter UI" for designing timber frame floor structures. It interfaces with the
cadwork
API to create beam structures with top and bottom boards based on polygon vertices and thickness information.

## Features

- Configure beam dimensions (width, height, spacing)
- Configure board thicknesses (top and bottom)
- Define element names and colors
- Generate complete floor structure with beams and boards

## Project Structure

The application is organized into several modules:

- `ui/` - UI components and main application window
- `models/` - Data structures and business logic
- `controllers/` - Application controllers
- `cad_adapter/` - CAD software API integration

## Implementation Requirements

Students are required to implement the function bodies in the `cad_adapter/adapter_api_wrappers.py` file. These
functions serve as the integration layer between the application and the CAD software. The functions currently contain
`NotImplementedError` placeholders that need to be replaced with actual implementations.

Key functions to implement include:

- Element selection and filtering
- Point manipulation and vector operations
- Element property retrieval (width, height, coordinates)
- Element creation (beams, panels, nodes)
- Element attribute setting (color, name)

## Getting Started

1. Clone this repository or download the ZIP file
2. Review the `cad_adapter/adapter_api_wrappers.py` file to understand the required API interfaces
3. Implement the function bodies in the adapter file
4. Run the application via `bfh_timber_framed_slab.py` therefore craete a directory in cadwork's `API.x64` folder with
   the name `bfh_timber_framed_slab`

## Dependencies

- Python 3.10+
- Tkinter for UI
- Access to the CAD software API (specific to your environment)