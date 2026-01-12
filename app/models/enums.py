"""
Enumerations for the PPTX API
"""
from enum import Enum


class TextAlignment(str, Enum):
    """Text alignment options"""
    LEFT = "LEFT"
    CENTER = "CENTER"
    RIGHT = "RIGHT"
    JUSTIFY = "JUSTIFY"
    DISTRIBUTE = "DISTRIBUTE"


class VerticalAlignment(str, Enum):
    """Vertical alignment options"""
    TOP = "TOP"
    MIDDLE = "MIDDLE"
    BOTTOM = "BOTTOM"
