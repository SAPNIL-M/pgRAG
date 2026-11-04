from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import computed_field


class Settings(BaseSettings):
    POSTGRES_USER: str = "rag_user"
    POSTGRES_PASSWORD: str = "rag_password"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "rag_db"
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-mpnet-base-v2"

    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

    @computed_field
    @property
    def database_url(self)->str:
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
                )

settings=Settings()