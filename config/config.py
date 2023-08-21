from typing_extensions import Literal
from pydantic import BaseConfig

PHASE = Literal["dev", "qa", "alpha", "prod"]

#JWT
ACCESS_TOKEN_EXPIRE_M = 30
REFRESH_TOKEN_EXPIRE_M = 60 * 24
ALGORITHM = "HS256"
JWT_SECRET_KEY = "access_secret"
JWT_REFRESH_SECRET_KEY = "refresh_secret"


class DefaultConfig(BaseConfig):
    app_name: str = "on-boarding Project"
    author: str = "Enrique"
    author_email: str = "enrique@aimmo.co.kr"


class DevelopConfig(DefaultConfig):
    phase: PHASE = "dev"
    mongo_url: str = "mongodb://localhost:27017/on_board"


class ProductConfig(DefaultConfig):
    phase: PHASE = "prod"
