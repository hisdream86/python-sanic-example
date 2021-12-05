import importlib
import os


STAGE = os.environ.get("APP_ENV", "LOCAL")

try:
    config = importlib.import_module(f"configs.{STAGE.lower()}").Config
except ModuleNotFoundError:
    config = importlib.import_module(f"configs.default").BaseConfig
