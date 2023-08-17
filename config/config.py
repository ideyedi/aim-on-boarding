from typing_extensions import Literal
from pydantic import BaseConfig

PHASE = Literal["dev", "qa", "alpha", "prod"]


class DefaultConfig(BaseConfig):
    app_name: str = "on-boarding Project"
    author: str = "Enrique"
    author_email: str = "enrique@aimmo.co.kr"


class DevelopConfig(DefaultConfig):
    phase: PHASE = "dev"
    mongoUrl: str = "mongodb://localhost:27017/on_board"


class ProductConfig(DefaultConfig):
    phase: PHASE = "prod"
