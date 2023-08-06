from sanic.log import access_logger
from sanic.response import HTTPResponse


class LogResponseMixin:
    def log_response(self, response) -> None:
        if self.access_log:
            extra = self.extra_log_response_fields(response=response)
            assert isinstance(extra, dict)

            extra["status"] = getattr(response, "status", 0)

            if isinstance(response, HTTPResponse):
                extra["byte"] = len(response.body)
            else:
                extra["byte"] = -1

            extra["host"] = "UNKNOWN"
            if self.request is not None:
                if self.request.ip:
                    extra["host"] = "{0}:{1}".format(
                        self.request.ip, self.request.port
                    )

                extra["request"] = "{0} {1}".format(
                    self.request.method, self.request.url
                )
                if 'id' in self.request:
                    extra['request_id'] = str(self.request['id'])
            else:
                extra["request"] = "nil"

            access_logger.info("", extra=extra)

    def extra_log_response_fields(self, response) -> dict:
        return {}
