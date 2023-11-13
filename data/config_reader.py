from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, PositiveInt, StrictStr


class Settings(BaseSettings):
    bot_token: SecretStr
    secret_key: SecretStr
    admin: PositiveInt
    redis_url: StrictStr

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()
