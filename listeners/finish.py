import sanic
import uvloop

from clients import HTTPBaseClient


async def finish(app: sanic.app.Sanic, loop: uvloop.Loop) -> None:
    await HTTPBaseClient.close_session(loop=loop)
