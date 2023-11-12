from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    SMARTY_AUTH_ID: str
    SMARTY_AUTH_TOKEN: str
    AIRTABLE_TOKEN: str
    AIRTABLE_TOKEN_ID: str
    AIRTABLE_BASE_ID: str
    AIRTABLE_TABLE_ID: str
    AIRTABLE_VIEW_ID: str
    GEOCODER_AUTH_KEY: str

    class Config:
        env_file = '.env'


# https://fastapi.tiangolo.com/advanced/settings/
