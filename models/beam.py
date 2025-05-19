#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Beam model for timber frame construction.
"""


class Beam:
    def __init__(self, width, height, length, start_point, end_point, color="#8B4513", name="Beam"):
        self.width = width
        self.height = height
        self.length = length
        self.start_point = start_point
        self.end_point = end_point
        self.color = color
        self.name = name
    
    def get_volume(self):
        return self.width * self.height * self.length
    
    def to_dict(self):
        return {
            "width": self.width,
            "height": self.height,
            "length": self.length,
            "start_point": self.start_point,
            "end_point": self.end_point,
            "color": self.color,
            "name": self.name
        }