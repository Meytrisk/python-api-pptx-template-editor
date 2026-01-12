"""
Pydantic schemas for request/response models
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from .enums import TextAlignment, VerticalAlignment


class Position(BaseModel):
    """Position coordinates"""
    left: float
    top: float


class Size(BaseModel):
    """Size dimensions"""
    width: float
    height: float


class VariableInfo(BaseModel):
    """Information about a variable detected in a template"""
    name: str = Field(..., description="Variable name (without the curly braces)")
    type: str = Field(..., description="Type of variable (text or image)")
    slide_index: int = Field(..., description="Index of the slide where the variable was found")


class TemplateVariables(BaseModel):
    """All variables detected in a template"""
    template_id: str
    variables: List[VariableInfo]


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
    """Request to insert text into a variable"""
    variable_name: str = Field(..., description="Variable name to replace (without {{}})")
    text: str = Field(..., min_length=1, description="Text content to insert")
    formatting: Optional[TextFormatting] = Field(None, description="Optional text formatting")


class ImageInsertRequest(BaseModel):
    """Request to insert an image into a variable"""
    variable_name: str = Field(..., description="Variable name to replace (from Alt Text)")


class TemplateInfo(BaseModel):
    """Basic information about a template"""
    template_id: str
    filename: str

class TemplateListResponse(BaseModel):
    """Response containing a list of templates"""
    templates: List[TemplateInfo]


class TemplateUploadResponse(BaseModel):
    """Response after uploading a template"""
    template_id: str = Field(..., description="Unique template identifier")
    filename: str = Field(..., description="Original filename")
    message: str = Field(..., description="Success message")


class PresentationCreateRequest(BaseModel):
    """Request to create a presentation from a template"""
    template_id: str = Field(..., description="Template ID to use")


class PresentationInfo(BaseModel):
    """Basic information about a presentation"""
    presentation_id: str
    template_id: Optional[str] = None
    filename: str

class PresentationListResponse(BaseModel):
    """Response containing a list of presentations"""
    presentations: List[PresentationInfo]


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
