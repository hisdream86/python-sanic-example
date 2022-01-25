import time
import uuid

from sanic.request import Request
from utils import logger


async def default_request_middleware(request: Request):
    request.ctx.request_id = request.headers.get("request-id", request.headers.get("request-id")) or str(uuid.uuid4())
    request.ctx.start = time.time()
    logger.request(request)
