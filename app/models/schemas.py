"""
Pydantic schemas for request/response models
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from .enums import PlaceholderType, TextAlignment, VerticalAlignment


class Position(BaseModel):
    """Position coordinates"""
    left: float
    top: float


class Size(BaseModel):
    """Size dimensions"""
    width: float
    height: float


class PlaceholderInfo(BaseModel):
    """Information about a placeholder in a slide"""
    idx: int = Field(..., description="Placeholder index")
    name: str = Field(..., description="Placeholder name")
    type: PlaceholderType = Field(..., description="Placeholder type")
    position: Optional[Position] = None
    size: Optional[Size] = None


class SlidePlaceholders(BaseModel):
    """Placeholders in a slide"""
    slide_index: int
    placeholders: List[PlaceholderInfo]


class TemplatePlaceholders(BaseModel):
    """All placeholders in a template"""
    template_id: str
    slides: List[SlidePlaceholders]


class TextFormatting(BaseModel):
    """Text formatting options"""
    font_name: Optional[str] = Field(None, description="Font family name")
    font_size: Optional[int] = Field(None, ge=1, le=400, description="Font size in points")
    bold: Optional[bool] = Field(None, description="Bold text")
    italic: Optional[bool] = Field(None, description="Italic text")
    underline: Optional[bool] = Field(None, description="Underline text")
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$', description="Hex color code (e.g., #FF0000)")
    alignment: Optional[TextAlignment] = Field(None, description="Text alignment")
    vertical_alignment: Optional[VerticalAlignment] = Field(None, description="Vertical alignment")


class TextInsertRequest(BaseModel):
    """Request to insert text into a placeholder"""
    placeholder_name: str = Field(..., description="Placeholder name to insert text into")
    text: str = Field(..., min_length=1, description="Text content to insert")
    formatting: Optional[TextFormatting] = Field(None, description="Optional text formatting")


class ImageInsertRequest(BaseModel):
    """Request to insert an image into a placeholder"""
    placeholder_name: str = Field(..., description="Alt Text of the image to replace")


class TemplateUploadResponse(BaseModel):
    """Response after uploading a template"""
    template_id: str = Field(..., description="Unique template identifier")
    filename: str = Field(..., description="Original filename")
    message: str = Field(..., description="Success message")


class PresentationCreateRequest(BaseModel):
    """Request to create a presentation from a template"""
    template_id: str = Field(..., description="Template ID to use")


class PresentationCreateResponse(BaseModel):
    """Response after creating a presentation"""
    presentation_id: str = Field(..., description="Unique presentation identifier")
    template_id: str = Field(..., description="Template ID used")
    message: str = Field(..., description="Success message")


class ContentInsertResponse(BaseModel):
    """Response after inserting content"""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Success or error message")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="API status")
    version: str = Field(..., description="API version")
