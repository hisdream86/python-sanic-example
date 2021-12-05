import sanic
import uvloop

from clients import HTTPBaseClient


async def init(app: sanic.app.Sanic, loop: uvloop.Loop) -> None:
    HTTPBaseClient.create_session(loop=loop)
