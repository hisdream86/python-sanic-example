import multiprocessing

from config.default import BaseConfig


class Config(BaseConfig):
    NUM_WORKERS = int(multiprocessing.cpu_count()) + 1
    ALLOWED_ORIGINS = [
        # Specify your allowed origins (ex. http://localhost:3000)
    ]
