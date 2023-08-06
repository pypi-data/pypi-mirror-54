from uuid import uuid4

from sanic.request import Request


def ensure_request_id(request: Request):
    request_id = request.headers.get('x-request-id')
    if not request_id:
        request_id = uuid4()
    request['id'] = request_id


def return_request_id_header(request, response):
    if 'id' in request:
        response.headers['X-Request-Id'] = request['id']
