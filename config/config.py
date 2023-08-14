from typing_extensions import Literal
from pydantic import BaseConfig

PHASE = Literal["dev", "qa", "alpha", "prod"]


class DefaultConfig(BaseConfig):
    app_name: str = "on-boarding POST"
    author: str = "Enrique"
    author_email: str = "enrique@aimmo.co.kr"
