#pylint: disable=E0611, C0116, C0103, E0213
#pylint: disable=R0903
""" Settings module for environment variables
"""
import secrets
from typing   import List, Optional, Dict, Any
from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator
# development enviroments (stages)
from .enums   import Environments


current_env = Environments.DEVELOP


class Settings(BaseSettings):
    """ Config enviroment variables class
    """


    API_V1_STR: str = "/api/v1"
    #SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int              = 60 * 24 * 5 # 5 days
    CURRENT_SCHEMA             : str              = Environments(current_env.value).name
    BACKEND_CORS_ORIGINS       : List[AnyHttpUrl] = []

    POSTGRES_SERVER     : str
    POSTGRES_USER       : str
    POSTGRES_PASSWORD   : str
    POSTGRES_DB         : str
    DATABASE_URI        : Optional[PostgresDsn] = None
    IMAGE_SERVER_URL    : str
    USER_HASHED_PASSWORD: str

    ADMIN_USER_EMAIL: str


    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme   = "postgres",
            user     = values.get("POSTGRES_USER"),
            password = values.get("POSTGRES_PASSWORD"),
            host     = values.get("POSTGRES_SERVER"),
            path     = f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        """
        Additional configuration settings for the parent Settings class.
        """
        env_file = current_env.value


settings = Settings()
