from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class LLMSettings(BaseSettings):
    OPENAI_API_KEY: str
    CHROMA_DB_DIR: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


