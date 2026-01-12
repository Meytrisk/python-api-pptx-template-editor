"""
File service for handling template, image, and presentation files
"""
import os
import shutil
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException


class FileService:
    """Service for managing file operations"""
    
    def __init__(self, base_dir: str = "."):
        """
        Initialize file service
        
        Args:
            base_dir: Base directory for the application
        """
        self.base_dir = Path(base_dir)
        self.templates_dir = self.base_dir / "uploads" / "templates"
        self.images_dir = self.base_dir / "uploads" / "images"
        self.outputs_dir = self.base_dir / "outputs"
        
        # Create directories if they don't exist
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories"""
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_id(self) -> str:
        """Generate a unique ID"""
        return str(uuid.uuid4())
    
    async def save_template(self, file: UploadFile) -> tuple[str, str]:
        """
        Save an uploaded template file
        
        Args:
            file: Uploaded file object
            
        Returns:
            Tuple of (template_id, filename)
            
        Raises:
            HTTPException: If file is invalid
        """
        # Validate file extension
        if not file.filename or not file.filename.lower().endswith('.pptx'):
            raise HTTPException(
                status_code=400,
                detail="Invalid file format. Only .pptx files are allowed."
            )
        
        # Generate unique ID
        template_id = self.generate_id()
        
        # Create file path
        file_extension = Path(file.filename).suffix
        filename = f"{template_id}{file_extension}"
        file_path = self.templates_dir / filename
        
        # Save file
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save template: {str(e)}"
            )
        
        return template_id, filename
    
    async def save_image(self, file: UploadFile) -> tuple[str, str]:
        """
        Save an uploaded image file
        
        Args:
            file: Uploaded file object
            
        Returns:
            Tuple of (image_id, filename)
            
        Raises:
            HTTPException: If file is invalid
        """
        # Validate file extension
        allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}
        if not file.filename or Path(file.filename).suffix.lower() not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image format. Allowed formats: {', '.join(allowed_extensions)}"
            )
        
        # Generate unique ID
        image_id = self.generate_id()
        
        # Create file path
        file_extension = Path(file.filename).suffix
        filename = f"{image_id}{file_extension}"
        file_path = self.images_dir / filename
        
        # Save file
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save image: {str(e)}"
            )
        
        return image_id, filename
    
    def get_template_path(self, template_id: str) -> Path:
        """
        Get the path to a template file
        
        Args:
            template_id: Template ID
            
        Returns:
            Path to template file
            
        Raises:
            HTTPException: If template not found
        """
        # Find template file
        for file_path in self.templates_dir.glob(f"{template_id}.*"):
            if file_path.is_file():
                return file_path
        
        raise HTTPException(
            status_code=404,
            detail=f"Template with ID '{template_id}' not found"
        )
    
    def get_image_path(self, image_id: str) -> Path:
        """
        Get the path to an image file
        
        Args:
            image_id: Image ID
            
        Returns:
            Path to image file
            
        Raises:
            HTTPException: If image not found
        """
        # Find image file
        for file_path in self.images_dir.glob(f"{image_id}.*"):
            if file_path.is_file():
                return file_path
        
        raise HTTPException(
            status_code=404,
            detail=f"Image with ID '{image_id}' not found"
        )
    
    def create_presentation_path(self, presentation_id: str) -> Path:
        """
        Create a path for a presentation file
        
        Args:
            presentation_id: Presentation ID
            
        Returns:
            Path to presentation file
        """
        filename = f"{presentation_id}.pptx"
        return self.outputs_dir / filename
    
    def get_presentation_path(self, presentation_id: str) -> Path:
        """
        Get the path to a presentation file
        
        Args:
            presentation_id: Presentation ID
            
        Returns:
            Path to presentation file
            
        Raises:
            HTTPException: If presentation not found
        """
        file_path = self.create_presentation_path(presentation_id)
        
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Presentation with ID '{presentation_id}' not found"
            )
        
        return file_path
    
    def delete_template(self, template_id: str) -> bool:
        """
        Delete a template file
        
        Args:
            template_id: Template ID
            
        Returns:
            True if deleted successfully
        """
        file_path = self.get_template_path(template_id)
        try:
            file_path.unlink()
            return True
        except Exception:
            return False
    
    def delete_presentation(self, presentation_id: str) -> bool:
        """
        Delete a presentation file
        
        Args:
            presentation_id: Presentation ID
            
        Returns:
            True if deleted successfully
        """
        file_path = self.get_presentation_path(presentation_id)
        try:
            file_path.unlink()
            return True
        except Exception:
            return False
    
    def cleanup_image(self, image_id: str) -> bool:
        """
        Delete a temporary image file
        
        Args:
            image_id: Image ID
            
        Returns:
            True if deleted successfully
        """
        file_path = self.get_image_path(image_id)
        try:
            file_path.unlink()
            return True
        except Exception:
            return False

    def list_templates(self) -> list[dict]:
        """
        List all available templates
        
        Returns:
            List of dictionaries containing template information
        """
        templates = []
        for file_path in self.templates_dir.glob("*.pptx"):
            if file_path.is_file():
                templates.append({
                    "template_id": file_path.stem,
                    "filename": file_path.name
                })
        return templates

    def list_presentations(self) -> list[dict]:
        """
        List all available presentations
        
        Returns:
            List of dictionaries containing presentation information
        """
        presentations = []
        for file_path in self.outputs_dir.glob("*.pptx"):
            if file_path.is_file():
                presentations.append({
                    "presentation_id": file_path.stem,
                    "filename": file_path.name
                })
        return presentations
