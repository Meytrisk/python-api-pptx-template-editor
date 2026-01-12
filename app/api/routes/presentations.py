"""
Presentation endpoints for the PPTX API
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Form
from fastapi.responses import FileResponse
from pathlib import Path

from app.models.schemas import (
    PresentationCreateRequest,
    PresentationCreateResponse,
    PresentationListResponse,
    TextInsertRequest,
    ImageInsertRequest,
    VideoInsertRequest,
    ContentInsertResponse
)
from app.services.file_service import FileService
from app.services.pptx_service import PPTXService


router = APIRouter(prefix="/api/v1/presentations", tags=["presentations"])


@router.get(
    "/",
    response_model=PresentationListResponse,
    summary="List all presentations",
    description="Get a list of all PowerPoint presentations currently stored on the server"
)
async def list_presentations():
    """
    List all available presentations
    
    Returns a list of presentations with their IDs and filenames.
    """
    try:
        file_service = FileService()
        presentations = file_service.list_presentations()
        return PresentationListResponse(presentations=presentations)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list presentations: {str(e)}"
        )


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
    description="Scan the document and replace all instances of {{variable_name}} with the provided text."
)
async def insert_text(presentation_id: str, request: TextInsertRequest):
    """
    Replace text variables in the presentation
    
    - **presentation_id**: ID of the presentation
    - **variable_name**: Name of the variable to replace (without {{}})
    - **text**: Text content to insert
    - **formatting**: Optional text formatting (font, size, color, alignment, etc.)
    
    The API will look for {{variable_name}} throughout the entire presentation.
    """
    try:
        file_service = FileService()
        pptx_service = PPTXService(file_service)
        
        # Insert text
        pptx_service.insert_text(
            presentation_id=presentation_id,
            variable_name=request.variable_name,
            text=request.text,
            formatting=request.formatting
        )
        
        return ContentInsertResponse(
            success=True,
            message=f"Variable '{{{{{request.variable_name}}}}}' replaced successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to replace text variable: {str(e)}"
        )


@router.post(
    "/{presentation_id}/image",
    response_model=ContentInsertResponse,
    summary="Replace an image variable in the presentation",
    description="Replace an existing image whose Alt Text matches {{variable_name}} or {{image:variable_name}}."
)
async def insert_image(
    presentation_id: str,
    variable_name: str = Form(..., description="Variable name to replace (without {{}})"),
    image: UploadFile = File(..., description="Image file to insert")
):
    """
    Replace an image identifying it by its Alt Text variable.
    
    - **presentation_id**: ID of the presentation
    - **variable_name**: Name of the variable (will search for {{variable_name}} or {{image:variable_name}} in Alt Text)
    - **image**: Image file to insert (PNG, JPG, JPEG, GIF, BMP, TIFF)
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
            variable_name=variable_name,
            image_path=image_path
        )
        
        # Cleanup temporary image file
        file_service.cleanup_image(image_id)
        
        return ContentInsertResponse(
            success=True,
            message=f"Image variable '{{{{{variable_name}}}}}' replaced successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to replace image variable: {str(e)}"
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


@router.post(
    "/{presentation_id}/video",
    response_model=ContentInsertResponse,
    summary="Replace a video variable in the presentation",
    description="Replace an existing shape whose Alt Text matches {{variable_name}} or {{video:variable_name}}."
)
async def insert_video(
    presentation_id: str,
    variable_name: str = Form(..., description="Variable name to replace (without {{}} )"),
    video: UploadFile = File(..., description="Video file to insert (.mp4)"),
    poster: Optional[UploadFile] = File(None, description="Optional poster frame image")
):
    """
    Replace a shape with a video identifying it by its Alt Text variable.
    
    - **presentation_id**: ID of the presentation
    - **variable_name**: Name of the variable (will search for {{variable_name}} or {{video:variable_name}} in Alt Text)
    - **video**: Video file to insert (.mp4)
    - **poster**: Optional poster frame image. If not provided, it will be extracted from the video.
    """
    try:
        file_service = FileService()
        pptx_service = PPTXService(file_service)
        
        # Save video
        video_id, video_filename = await file_service.save_video(video)
        video_path = file_service.get_video_path(video_id)
        
        # Determine poster path
        poster_path = None
        if poster:
            # Save user-provided poster
            poster_id, poster_filename = await file_service.save_image(poster)
            poster_path = file_service.get_image_path(poster_id)
        else:
            # Extract automatic poster
            poster_path = file_service.extract_poster_frame(video_path)
            
        # Insert video
        pptx_service.insert_video(
            presentation_id=presentation_id,
            variable_name=variable_name,
            video_path=str(video_path),
            poster_path=str(poster_path)
        )
        
        return ContentInsertResponse(
            success=True,
            message=f"Video variable '{{{{{variable_name}}}}}' replaced successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to replace video variable: {str(e)}"
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
