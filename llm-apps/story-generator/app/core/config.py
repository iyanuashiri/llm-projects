from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

from decouple import config 


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        populate_by_name=True,
        env_file=".env",
        extra="ignore",
    )

    openrouter_api_key: str = Field(default=config("OPENROUTER_API_KEY"), 
                                    alias="OPENROUTER_API_KEY")
    database_url: str = Field(default=f"sqlite:///{config("STORY_GENERATOR_SQLITE_FILE_NAME")}", 
                              alias="DATABASE_URL") 

    @property
    def DATABASE_URL(self) -> str:
        return self.database_url

    @property
    def OPENROUTER_API_KEY(self) -> str:
        return self.openrouter_api_key


settings = Settings()
