from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    db_host: str
    db_name: str
    user: str
    password: str
    db_port: str
    admin_login: str
    admin_password: str
    # MYSQL_ROOT_PASSWORD: str
    # MYSQL_DATABASE: str
    # MYSQL_USER: str
    # MYSQL_PASSWORD: str
    
    @property
    def db_url(self):
        # return f"mysql+asyncmy://dak:200209318Dak()@db:3306/papa_task"?
        return f"mysql+asyncmy://{self.user}:{self.password}@{self.db_host}:{self.db_port}/{self.db_name}"
        
settings = Settings()
