"""
Enumerations for the PPTX API
"""
from enum import Enum


class PlaceholderType(str, Enum):
    """Placeholder types in PowerPoint"""
    TITLE = "TITLE"
    BODY = "BODY"
    PICTURE = "PICTURE"
    CENTER_TITLE = "CENTER_TITLE"
    SUBTITLE = "SUBTITLE"
    OBJECT = "OBJECT"
    CHART = "CHART"
    TABLE = "TABLE"
    DATE = "DATE"
    SLIDE_NUMBER = "SLIDE_NUMBER"
    FOOTER = "FOOTER"
    HEADER = "HEADER"
    UNKNOWN = "UNKNOWN"


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
