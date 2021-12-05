import time
import uuid

from sanic.request import Request
from utils import logger


async def handle_request(request: Request):
    request.ctx.request_id = request.headers.get("x-request-id", request.headers.get("request-id")) or str(uuid.uuid4())
    request.ctx.start = time.time()

    # For ignore non-http requests
    if request.method == "NONE":
        request.ctx.ping = True
        return await request.respond()

    logger.request(request)
