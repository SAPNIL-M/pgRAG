from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import computed_field


class Settings(BaseSettings):
    POSTGRES_USER: str = "rag_user"
    POSTGRES_PASSWORD: str = "rag_password"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "rag_db"
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-mpnet-base-v2"
    LLM_PROVIDER: str = "ollama"
    GEMINI_API_KEY:str |None = None
    GEMINI_MODEL:str = "gemini-2.0-flash"
    OLLAMA_BASE_URL:str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:3b"

    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

    @computed_field
    @property
    def database_url(self)->str:
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
                )

settings=Settings()