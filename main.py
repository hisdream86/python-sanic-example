from app import create_app
from configs import config

if __name__ == "__main__":
    app = create_app()
    app.run(
        host=config.HOST,
        port=config.PORT,
        workers=config.NUM_WORKERS,
        auto_reload=config.AUTO_RELOAD,
        access_log=False,
    )
