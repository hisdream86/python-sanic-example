from app import App
from config import config

if __name__ == "__main__":
    App().run(
        access_log=config.ACCESS_LOG,
        auto_reload=config.AUTO_RELOAD,
        host=config.HOST,
        port=config.PORT,
        workers=config.NUM_WORKERS,
    )
