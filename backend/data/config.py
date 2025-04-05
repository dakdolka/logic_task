from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    
    db_host: str
    db_name: str
    user: str
    password: str
    db_port: str
    
    @property
    def db_url(self):
        return f"mysql+asyncmy://{self.user}:{self.password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    class Config:
        env_file = f'{os.path.join(os.path.dirname(__file__), ".env")}'
        
settings = Settings()
