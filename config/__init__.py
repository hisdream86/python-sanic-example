import importlib
import os


STAGE = os.environ.get("STAGE", "LOCAL")

try:
    config = importlib.import_module(f"config.{STAGE.lower()}").Config
except ModuleNotFoundError:
    config = importlib.import_module("config.default").BaseConfig
