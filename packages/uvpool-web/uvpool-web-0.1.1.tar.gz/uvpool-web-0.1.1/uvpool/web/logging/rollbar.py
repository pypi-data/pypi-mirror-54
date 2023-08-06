import logging
import os

import rollbar.logger
from sanic import Sanic


def add_rollbar_logging(app: Sanic, code_version=None):
    if app.config.ENVIRONMENT.lower() in ['development', 'testing']:
        return
    access_token = os.getenv('ROLLBAR_ACCESS_TOKEN', None)
    if not access_token:
        logging.warn('Rollbar access token not provided, handlers will not be set')
        return
    kwargs = {}
    if code_version:
        kwargs['code_version'] = code_version
    handler = rollbar.logger.RollbarHandler(
        access_token=access_token,
        environment=app.config.ENVIRONMENT.lower(),
        level=logging.WARN,
        **kwargs
    )

    logging.getLogger('sanic.root').addHandler(handler)
    logging.getLogger('sanic.error').addHandler(handler)
