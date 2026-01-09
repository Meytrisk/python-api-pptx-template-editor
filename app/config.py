from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    """Application settings"""
    
    API_TITLE: str = "PPTX API"
    API_VERSION: str = "1.0.0"
    
    # CORS Settings
    # En producción, cambia esto a una lista de dominios específicos: ["https://tuapp.com"]
    CORS_ORIGINS: List[str] = ["*"]
    
    # Path Settings (se pueden sobreescribir con vars de entorno)
    BASE_DIR: str = "."
    UPLOAD_DIR: str = "uploads"
    OUTPUT_DIR: str = "outputs"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

settings = Settings()
