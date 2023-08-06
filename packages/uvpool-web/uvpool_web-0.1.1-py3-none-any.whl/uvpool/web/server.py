import os
from argparse import ArgumentParser

from sanic import Sanic
from sanic.server import HttpProtocol as BaseHttpProtocol
from sanic.websocket import WebSocketProtocol as BaseWebSocketProtocol

from uvpool.web.logging.protocol import LogResponseMixin


class HttpProtocol(LogResponseMixin, BaseHttpProtocol):
    pass


class WebSocketProtocol(LogResponseMixin, BaseWebSocketProtocol):
    pass


class Server:
    app_prefix = 'SANIC'
    argument_parser = None

    @classmethod
    def get_argument_parser(cls) -> ArgumentParser:
        if not cls.argument_parser:
            parser = ArgumentParser(prog='')
            # Server settings
            parser.add_argument('--host', default=os.getenv(f'{cls.app_prefix}_HOST', '0.0.0.0'), type=str,
                                help='Specify an interface this app should listen on, default: 0.0.0.0')
            parser.add_argument('--port', default=int(os.getenv(f'{cls.app_prefix}_PORT', 8080)), type=str,
                                help='Specify a port this app should listen on, default: 8080')
            parser.add_argument('--workers', default=int(os.getenv(f'{cls.app_prefix}_WORKERS', 1)), type=int,
                                help='Set worker count, default: 1')
            parser.add_argument('--debug', action='store_true', default=bool(os.getenv('DEBUG')),
                                help='Set debug mode')
            cls.argument_parser = parser

        return cls.argument_parser

    def __init__(self):
        self.args, _ = self.get_argument_parser().parse_known_args()

    @property
    def app(self) -> Sanic:
        from uvpool.web.app import app
        return app

    def serve(self) -> None:
        if self.app is None:
            raise ValueError('The app parameter must be set')
        if not isinstance(self.app, Sanic):
            raise ValueError('Server.app must be an instance of Sanic')

        self.app.run(
            host=self.args.host,
            port=self.args.port,
            debug=self.args.debug,
            workers=self.args.workers,
            protocol=HttpProtocol,
        )
