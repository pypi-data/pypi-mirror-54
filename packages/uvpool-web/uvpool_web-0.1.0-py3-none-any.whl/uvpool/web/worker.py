from sanic.worker import GunicornWorker as BaseGunicornWorker

from uvpool.web.server import HttpProtocol, WebSocketProtocol


class GunicornWorker(BaseGunicornWorker):
    http_protocol = HttpProtocol
    websocket_protocol = WebSocketProtocol
