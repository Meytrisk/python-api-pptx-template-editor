"""
Main FastAPI application for PPTX API
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import templates, presentations
from app.api.deps import verify_token
from app.models.schemas import HealthResponse
from app.config import settings


# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description="API for creating and modifying PowerPoint presentations using python-pptx",
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# Include routers with security dependency
app.include_router(
    templates.router,
    dependencies=[Depends(verify_token)]
)
app.include_router(
    presentations.router,
    dependencies=[Depends(verify_token)]
)


@app.get("/", response_model=HealthResponse, tags=["health"])
async def root():
    """
    Root endpoint - Health check
    
    Returns the API status and version information.
    """
    return HealthResponse(
        status="healthy",
        version=settings.API_VERSION
    )


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """
    Health check endpoint
    
    Returns the API status and version information.
    """
    return HealthResponse(
        status="healthy",
        version=settings.API_VERSION
    )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled exceptions
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "details": "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
