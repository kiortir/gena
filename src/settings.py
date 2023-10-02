from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class PGSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="db")
    
    user: str = "postgres"
    password: SecretStr = SecretStr("postgres")
    host: str = "localhost"
    port: int = 5432
    database: str = "postgres"
    
    driver: str = "postgres"
    
    @property
    def url(self) -> str:
        s = f"{self.driver}://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}"
        print(s)
        return s
    