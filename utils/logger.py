import time
import json
import traceback

from datetime import datetime
from pytz import timezone
from sanic.log import logger
from sanic.request import Request
from sanic.response import HTTPResponse
from configs import config

TZ_SEOUL = timezone("Asia/Seoul")


class Log:
    def __init__(self, level: str, type: str):
        self.app = config.APP_NAME
        self.level = level
        self.type = type
        self.datetime = datetime.now(TZ_SEOUL).isoformat("T")

    def format(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False)


class RequestLog(Log):
    def __init__(self, request: Request):
        super().__init__("info", "request")
        self.request_id = request.ctx.request_id
        self.method = request.method
        self.url = request.path
        self.datetime = datetime.fromtimestamp(request.ctx.start, TZ_SEOUL).isoformat("T")
        self.headers = dict(request.headers)


class ResponseLog(Log):
    def __init__(self, request: Request, response: HTTPResponse, write_body=True):
        super().__init__("info", "response")
        self.request_id = request.ctx.request_id
        self.status = response.status

        if response.body and write_body:
            try:
                self.data = json.loads(response.body)
            except json.decoder.JSONDecodeError:
                self.data = response.body.decode("utf-8")

        self.latency = (time.time() - request.ctx.start) * 1000


class MessageLog(Log):
    def __init__(self, level: str, message: str):
        super().__init__(level, "info")
        self.message = message


class ErrorLog(Log):
    def __init__(self, message: str, exception: Exception, request: Request):
        super().__init__("error", "error")
        self.message = message
        self.stacktrace = traceback.format_exc() if exception else None


def request(request: Request):
    logger.info(RequestLog(request).format())


def response(request: Request, response: HTTPResponse, write_body=True):
    logger.info(ResponseLog(request, response, write_body).format())


def debug(message: str = ""):
    logger.debug(MessageLog("debug", message).format())


def info(message: str = ""):
    logger.info(MessageLog("info", message).format())


def warning(message: str = ""):
    logger.info(MessageLog("warning", message).format())


def error(message: str = "", exception: Exception = None, request: Request = None):
    logger.info(ErrorLog(message, exception, request).format())
