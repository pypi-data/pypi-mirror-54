from sanic.response import json
from sanic.views import HTTPMethodView


class HealthView(HTTPMethodView):
    def get(self, request):
        return json({
            'api': {
                'version': request.app.config.VERSION,
                'sha1': request.app.config.SHA1,
            },
        })
