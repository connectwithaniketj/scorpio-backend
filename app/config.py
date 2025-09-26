from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    scorpio_base_url: str = "http://localhost:9090/ngsi-ld"  # default fallback

    class Config:
        env_file = ".env"   # local development

settings = Settings()
