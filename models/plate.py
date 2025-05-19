#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Board model for timber frame construction.
"""


class Plate:
    def __init__(self, thickness, polygon, color="#DEB887", name="Board", position="top"):
        self.thickness = thickness
        self.polygon = polygon
        self.color = color
        self.name = name
        self.position = position
        
    def get_area(self):
        return 0.0
    
    def get_volume(self):
        return self.get_area() * self.thickness
    
    def to_dict(self):
        return {
            "thickness": self.thickness,
            "polygon": self.polygon,
            "color": self.color,
            "name": self.name,
            "position": self.position
        }