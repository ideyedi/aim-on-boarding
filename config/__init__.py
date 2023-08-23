from .config import ProductConfig, DevelopConfig

configurations = {
    "develop": DevelopConfig,
    "product": ProductConfig,
    "default": DevelopConfig
}