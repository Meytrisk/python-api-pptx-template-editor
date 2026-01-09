"""
Template endpoints for the PPTX API
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import List

from app.models.schemas import (
    TemplateUploadResponse,
    TemplatePlaceholders,
    ErrorResponse,
    ContentInsertResponse
)
from app.services.file_service import FileService
from app.services.pptx_service import PPTXService


router = APIRouter(prefix="/api/v1/templates", tags=["templates"])


@router.post(
    "/upload",
    response_model=TemplateUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a PowerPoint template",
    description="Upload a .pptx file to be used as a template for creating presentations"
)
async def upload_template(
    file: UploadFile = File(..., description="PowerPoint template file (.pptx)")
):
    """
    Upload a PowerPoint template file
    
    - **file**: PowerPoint template file (.pptx format)
    
    Returns a template_id that can be used to create presentations.
    """
    try:
        file_service = FileService()
        template_id, filename = await file_service.save_template(file)
        
        return TemplateUploadResponse(
            template_id=template_id,
            filename=filename,
            message="Template uploaded successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload template: {str(e)}"
        )


@router.get(
    "/{template_id}/placeholders",
    response_model=TemplatePlaceholders,
    summary="Get placeholders from a template",
    description="Retrieve all placeholders from a template, including their types, names, and positions"
)
async def get_template_placeholders(template_id: str):
    """
    Get all placeholders from a template
    
    - **template_id**: Unique identifier of the template
    
    Returns information about all placeholders in the template, including:
    - Placeholder index (idx)
    - Placeholder name
    - Placeholder type (TITLE, BODY, PICTURE, etc.)
    - Position and size (if available)
    """
    try:
        file_service = FileService()
        pptx_service = PPTXService(file_service)
        
        placeholders = pptx_service.get_template_placeholders(template_id)
        
        return placeholders
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get placeholders: {str(e)}"
        )


@router.delete(
    "/{template_id}",
    response_model=ContentInsertResponse,
    summary="Delete a template",
    description="Delete a template from the server"
)
async def delete_template(template_id: str):
    """
    Delete a template
    
    - **template_id**: Unique identifier of the template to delete
    
    Returns success status if the template was deleted successfully.
    """
    try:
        file_service = FileService()
        
        success = file_service.delete_template(template_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template with ID '{template_id}' not found or could not be deleted"
            )
        
        return ContentInsertResponse(
            success=True,
            message=f"Template '{template_id}' deleted successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete template: {str(e)}"
        )
