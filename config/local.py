from .default import BaseConfig


class Config(BaseConfig):
    ALLOWED_ORIGINS = [
        # Specify your allowed origins (ex. http://localhost:3000)
    ]
    PORT = 8080
    NUM_WORKERS = 2
