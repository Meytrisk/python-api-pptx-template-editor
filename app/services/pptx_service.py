"""
PPTX service for PowerPoint presentation manipulation using python-pptx
"""
from pathlib import Path
from typing import List, Optional
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt
from pptx.dml.color import RGBColor

from app.models.schemas import (
    PlaceholderInfo,
    SlidePlaceholders,
    TemplatePlaceholders,
    TextFormatting
)
from app.models.enums import PlaceholderType, TextAlignment, VerticalAlignment
from app.services.file_service import FileService


class PPTXService:
    """Service for PowerPoint presentation operations"""
    
    def __init__(self, file_service: FileService):
        """
        Initialize PPTX service
        
        Args:
            file_service: File service instance
        """
        self.file_service = file_service
    
    def _get_placeholder_type(self, placeholder) -> PlaceholderType:
        """
        Get the type of a placeholder
        
        Args:
            placeholder: Placeholder object from python-pptx
            
        Returns:
            PlaceholderType enum value
        """
        try:
            placeholder_format_type = placeholder.placeholder_format.type
            
            # Map python-pptx placeholder types to our enum
            type_mapping = {
                0: PlaceholderType.TITLE,
                1: PlaceholderType.BODY,
                2: PlaceholderType.CENTER_TITLE,
                3: PlaceholderType.SUBTITLE,
                4: PlaceholderType.OBJECT,
                5: PlaceholderType.CHART,
                6: PlaceholderType.TABLE,
                7: PlaceholderType.DATE,
                8: PlaceholderType.SLIDE_NUMBER,
                9: PlaceholderType.FOOTER,
                10: PlaceholderType.HEADER,
                18: PlaceholderType.PICTURE,
            }
            
            return type_mapping.get(placeholder_format_type, PlaceholderType.UNKNOWN)
        except Exception:
            return PlaceholderType.UNKNOWN
    
    def get_template_placeholders(self, template_id: str) -> TemplatePlaceholders:
        """
        Get all placeholders from a template
        
        Args:
            template_id: Template ID
            
        Returns:
            TemplatePlaceholders object with all placeholder information
            
        Raises:
            Exception: If template cannot be loaded
        """
        # Get template path
        template_path = self.file_service.get_template_path(template_id)
        
        # Load presentation
        try:
            prs = Presentation(str(template_path))
        except Exception as e:
            raise Exception(f"Failed to load template: {str(e)}")
        
        # Extract placeholders from all slides
        slides_data = []
        
        for slide_idx, slide in enumerate(prs.slides):
            placeholders = []
            
            for placeholder in slide.placeholders:
                placeholder_info = PlaceholderInfo(
                    idx=placeholder.idx,
                    name=placeholder.name,
                    type=self._get_placeholder_type(placeholder)
                )
                
                # Add position and size if available
                try:
                    if hasattr(placeholder, 'left') and hasattr(placeholder, 'top'):
                        from app.models.schemas import Position, Size
                        placeholder_info.position = Position(
                            left=float(placeholder.left),
                            top=float(placeholder.top)
                        )
                    
                    if hasattr(placeholder, 'width') and hasattr(placeholder, 'height'):
                        from app.models.schemas import Size
                        placeholder_info.size = Size(
                            width=float(placeholder.width),
                            height=float(placeholder.height)
                        )
                except Exception:
                    pass
                
                placeholders.append(placeholder_info)
            
            if placeholders:
                slide_data = SlidePlaceholders(
                    slide_index=slide_idx,
                    placeholders=placeholders
                )
                slides_data.append(slide_data)
        
        return TemplatePlaceholders(
            template_id=template_id,
            slides=slides_data
        )
    
    def create_presentation(self, template_id: str, presentation_id: str) -> str:
        """
        Create a new presentation from a template
        
        Args:
            template_id: Template ID to use
            presentation_id: ID for the new presentation
            
        Returns:
            Path to the created presentation
            
        Raises:
            Exception: If presentation cannot be created
        """
        # Get template path
        template_path = self.file_service.get_template_path(template_id)
        
        # Load presentation from template
        try:
            prs = Presentation(str(template_path))
        except Exception as e:
            raise Exception(f"Failed to load template: {str(e)}")
        
        # Save presentation
        output_path = self.file_service.create_presentation_path(presentation_id)
        
        try:
            prs.save(str(output_path))
        except Exception as e:
            raise Exception(f"Failed to save presentation: {str(e)}")
        
        return str(output_path)
    
    def insert_text(
        self,
        presentation_id: str,
        placeholder_name: str,
        text: str,
        formatting: Optional[TextFormatting] = None
    ) -> bool:
        """
        Insert text into a placeholder in a presentation
        
        Args:
            presentation_id: Presentation ID
            placeholder_name: Placeholder name
            text: Text content to insert
            formatting: Optional text formatting
        
        Returns:
            True if successful
        
        Raises:
            Exception: If operation fails
        """
        # Get presentation path
        presentation_path = self.file_service.get_presentation_path(presentation_id)
        
        # Load presentation
        try:
            prs = Presentation(str(presentation_path))
        except Exception as e:
            raise Exception(f"Failed to load presentation: {str(e)}")
        
        # Find placeholder and insert text
        placeholder_found = False
        
        for slide in prs.slides:
            for placeholder in slide.placeholders:
                if placeholder.name == placeholder_name:
                    placeholder_found = True
                    
                    # Check if it's a text placeholder
                    placeholder_type = self._get_placeholder_type(placeholder)
                    
                    if placeholder_type == PlaceholderType.PICTURE:
                        raise Exception("Cannot insert text into a picture placeholder")
                    
                    # Insert text
                    try:
                        placeholder.text = text
                        
                        # Apply formatting if provided
                        if formatting:
                            self._apply_text_formatting(placeholder, formatting)
                    except Exception as e:
                        raise Exception(f"Failed to insert text: {str(e)}")
                    
                    break
            
            if placeholder_found:
                break
        
        if not placeholder_found:
            raise Exception(f"Placeholder with name '{placeholder_name}' not found")
        
        # Save presentation
        try:
            prs.save(str(presentation_path))
        except Exception as e:
            raise Exception(f"Failed to save presentation: {str(e)}")
        
        return True
    
    def _apply_text_formatting(self, placeholder, formatting: TextFormatting):
        """
        Apply text formatting to a placeholder
        
        Args:
            placeholder: Placeholder object
            formatting: TextFormatting object
        """
        try:
            text_frame = placeholder.text_frame
            
            # Apply text frame formatting
            if formatting.vertical_alignment:
                vertical_mapping = {
                    VerticalAlignment.TOP: MSO_ANCHOR.TOP,
                    VerticalAlignment.MIDDLE: MSO_ANCHOR.MIDDLE,
                    VerticalAlignment.BOTTOM: MSO_ANCHOR.BOTTOM
                }
                text_frame.vertical_anchor = vertical_mapping.get(
                    formatting.vertical_alignment,
                    MSO_ANCHOR.TOP
                )
            
            # Apply paragraph formatting
            if formatting.alignment:
                alignment_mapping = {
                    TextAlignment.LEFT: PP_ALIGN.LEFT,
                    TextAlignment.CENTER: PP_ALIGN.CENTER,
                    TextAlignment.RIGHT: PP_ALIGN.RIGHT,
                    TextAlignment.JUSTIFY: PP_ALIGN.JUSTIFY,
                    TextAlignment.DISTRIBUTE: PP_ALIGN.DISTRIBUTE
                }
                for paragraph in text_frame.paragraphs:
                    paragraph.alignment = alignment_mapping.get(
                        formatting.alignment,
                        PP_ALIGN.LEFT
                    )
            
            # Apply font formatting to all runs
            for paragraph in text_frame.paragraphs:
                for run in paragraph.runs:
                    font = run.font
                    
                    if formatting.font_name:
                        font.name = formatting.font_name
                    
                    if formatting.font_size:
                        font.size = Pt(formatting.font_size)
                    
                    if formatting.bold is not None:
                        font.bold = formatting.bold
                    
                    if formatting.italic is not None:
                        font.italic = formatting.italic
                    
                    if formatting.underline is not None:
                        font.underline = formatting.underline
                    
                    if formatting.color:
                        # Parse hex color
                        hex_color = formatting.color.lstrip('#')
                        r = int(hex_color[0:2], 16)
                        g = int(hex_color[2:4], 16)
                        b = int(hex_color[4:6], 16)
                        font.color.rgb = RGBColor(r, g, b)
        except Exception as e:
            raise Exception(f"Failed to apply formatting: {str(e)}")
    
    def insert_image(
        self,
        presentation_id: str,
        placeholder_name: str,
        image_path: str
    ) -> bool:
        """
        Insert an image into a presentation by replacing an existing image with matching Alt Text.
        
        Args:
            presentation_id: Presentation ID
            placeholder_name: The Alt Text to look for
            image_path: Path to the new image file
        
        Returns:
            True if successful
        
        Raises:
            Exception: If operation fails or Alt Text not found
        """
        # Get presentation path
        presentation_path = self.file_service.get_presentation_path(presentation_id)
        
        # Load presentation
        try:
            prs = Presentation(str(presentation_path))
        except Exception as e:
            raise Exception(f"Failed to load presentation: {str(e)}")
        
        image_replaced = False
        
        # Iterate through all slides to find the image with matching Alt Text
        for slide in prs.slides:
            # We need to iterate over a list copy because we might modify the shapes collection
            for shape in list(slide.shapes):
                # Check for Alt Text
                # python-pptx doesn't expose Alt Text directly in the high-level API for all versions
                # We need to access the XML element
                try:
                    # Generic way to get non-visual properties
                    nvPr = shape._element.nvXxPr
                    cNvPr = nvPr.find('p:cNvPr', namespaces=nvPr.nsmap)
                    if cNvPr is None:
                        # Fallback for some shape types
                        cNvPr = nvPr.find('*/p:cNvPr', namespaces=nvPr.nsmap)
                    
                    if cNvPr is not None:
                         alt_text = cNvPr.get("descr")
                         
                         if alt_text == placeholder_name:
                             # Found match!
                             image_replaced = True
                             
                             # Capture original geometry
                             left = shape.left
                             top = shape.top
                             width = shape.width
                             height = shape.height
                             
                             # Insert new picture at same position and size
                             try:
                                 new_picture = slide.shapes.add_picture(
                                     image_path, 
                                     left, 
                                     top, 
                                     width, 
                                     height
                                 )
                                 
                                 # Remove the original shape (reference image)
                                 sp = shape._element
                                 sp.getparent().remove(sp)
                                 
                             except Exception as e:
                                 raise Exception(f"Failed to replace image: {str(e)}")
                             
                             break
                except Exception:
                    # If we can't read properties or it's not a shape we can handle, skip
                    continue
            
            if image_replaced:
                break
        
        if not image_replaced:
            raise Exception(f"No image found with Alt Text '{placeholder_name}'")
        
        # Save presentation
        try:
            prs.save(str(presentation_path))
        except Exception as e:
            raise Exception(f"Failed to save presentation: {str(e)}")
        
        return True
