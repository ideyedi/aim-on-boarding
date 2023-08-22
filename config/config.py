from typing_extensions import Literal

from pydantic import BaseConfig
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

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

    APISPEC_SPEC = APISpec(
        title="On-boarding API swagger",
        version="v1.0",
        plugins=[
            MarshmallowPlugin(),
        ],
        openapi_version="3.0.2",
    )
    APISPEC_SWAGGER_URL = "/swagger-json"  # Corresponds to Documentation
    APISPEC_SWAGGER_UI_URL = "/swagger-api"  # Corresponds to MainSwagger UI


class DevelopConfig(DefaultConfig):
    phase: PHASE = "dev"
    mongo_url: str = "mongodb://localhost:27017/on_board"


class ProductConfig(DefaultConfig):
    phase: PHASE = "prod"
