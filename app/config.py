
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Platform Demo"
    MODEL_NAME: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    USE_GPU: bool = True  # 若有 CUDA 則會自動使用

    class Config:
        env_file = ".env"


settings = Settings()
