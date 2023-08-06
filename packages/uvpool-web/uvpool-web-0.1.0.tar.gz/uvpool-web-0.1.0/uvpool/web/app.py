from sanic import Sanic

from .global_settings import LOGGING_CONFIG


def create_app(log_config=None, **kwargs):
    kwargs.setdefault('name', 'UVPool Web server')
    _app = Sanic(log_config=log_config or LOGGING_CONFIG, **kwargs)
    _app.config.setdefault('ENVIRONMENT', 'development')

    return _app


def get_app():
    global default_app
    if default_app is None:
        default_app = create_app()
    return default_app


default_app = None
app = get_app()
