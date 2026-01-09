"""
Presentation endpoints for the PPTX API
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Form
from fastapi.responses import FileResponse
from pathlib import Path

from app.models.schemas import (
    PresentationCreateRequest,
    PresentationCreateResponse,
    TextInsertRequest,
    ImageInsertRequest,
    ContentInsertResponse
)
from app.services.file_service import FileService
from app.services.pptx_service import PPTXService


router = APIRouter(prefix="/api/v1/presentations", tags=["presentations"])


@router.post(
    "/create",
    response_model=PresentationCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a presentation from a template",
    description="Create a new presentation based on an uploaded template"
)
async def create_presentation(request: PresentationCreateRequest):
    """
    Create a new presentation from a template
    
    - **template_id**: ID of the template to use
    
    Returns a presentation_id that can be used to insert content and download the presentation.
    """
    try:
        file_service = FileService()
        pptx_service = PPTXService(file_service)
        
        # Generate presentation ID
        presentation_id = file_service.generate_id()
        
        # Create presentation from template
        pptx_service.create_presentation(request.template_id, presentation_id)
        
        return PresentationCreateResponse(
            presentation_id=presentation_id,
            template_id=request.template_id,
            message="Presentation created successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create presentation: {str(e)}"
        )


@router.post(
    "/{presentation_id}/text",
    response_model=ContentInsertResponse,
    summary="Insert text into a presentation",
    description="Insert text into a specific placeholder in the presentation"
)
async def insert_text(presentation_id: str, request: TextInsertRequest):
    """
    Insert text into a placeholder
    
    - **presentation_id**: ID of the presentation
    - **placeholder_name**: Name of the placeholder to insert text into
    - **text**: Text content to insert
    - **formatting**: Optional text formatting (font, size, color, alignment, etc.)
    
    The text will be inserted into the specified placeholder. Formatting is optional.
    """
    try:
        file_service = FileService()
        pptx_service = PPTXService(file_service)
        
        # Insert text
        pptx_service.insert_text(
            presentation_id=presentation_id,
            placeholder_name=request.placeholder_name,
            text=request.text,
            formatting=request.formatting
        )
        
        return ContentInsertResponse(
            success=True,
            message=f"Text inserted successfully into placeholder '{request.placeholder_name}'"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to insert text: {str(e)}"
        )


@router.post(
    "/{presentation_id}/image",
    response_model=ContentInsertResponse,
    summary="Insert an image into a presentation",
    description="Insert an image into a specific placeholder in the presentation. The image will replace an existing image with matching Alt Text."
)
async def insert_image(
    presentation_id: str,
    placeholder_name: str = Form(..., description="Placeholder name to insert image into"),
    image: UploadFile = File(..., description="Image file to insert")
):
    """
    Inserta una imagen en la presentación, reemplazando una imagen existente identificada por su **Texto Alternativo (Alt Text)**.
    - **presentation_id**: ID of the presentation
    - **placeholder_name**: Name of the placeholder to insert image into
    - **image**: Image file to insert (PNG, JPG, JPEG, GIF, BMP, TIFF)
    
    The image will replace the existing image with the specified Alt Text.
    Please ensure the template has an image with the corresponding Alt Text.
    """
    try:
        file_service = FileService()
        pptx_service = PPTXService(file_service)
        
        # Save image
        image_id, image_filename = await file_service.save_image(image)
        image_path = str(file_service.get_image_path(image_id))
        
        # Insert image
        pptx_service.insert_image(
            presentation_id=presentation_id,
            placeholder_name=placeholder_name,
            image_path=image_path
        )
        
        # Cleanup temporary image file
        file_service.cleanup_image(image_id)
        
        return ContentInsertResponse(
            success=True,
            message=f"Image inserted successfully into placeholder '{placeholder_name}'"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to insert image: {str(e)}"
        )


@router.get(
    "/{presentation_id}/download",
    summary="Download a presentation",
    description="Download the generated PowerPoint presentation file"
)
async def download_presentation(presentation_id: str):
    """
    Download a presentation
    
    - **presentation_id**: ID of the presentation to download
    
    Returns the PowerPoint file (.pptx) for download.
    """
    try:
        file_service = FileService()
        
        # Get presentation path
        presentation_path = file_service.get_presentation_path(presentation_id)
        
        # Return file
        return FileResponse(
            path=str(presentation_path),
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            filename=f"{presentation_id}.pptx"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to download presentation: {str(e)}"
        )


@router.delete(
    "/{presentation_id}",
    response_model=ContentInsertResponse,
    summary="Delete a presentation",
    description="Delete a presentation from the server"
)
async def delete_presentation(presentation_id: str):
    """
    Delete a presentation
    
    - **presentation_id**: ID of the presentation to delete
    
    Returns success status if the presentation was deleted successfully.
    """
    try:
        file_service = FileService()
        
        success = file_service.delete_presentation(presentation_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Presentation with ID '{presentation_id}' not found or could not be deleted"
            )
        
        return ContentInsertResponse(
            success=True,
            message=f"Presentation '{presentation_id}' deleted successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete presentation: {str(e)}"
        )
