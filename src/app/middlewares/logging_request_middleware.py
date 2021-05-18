import logging
from logging import getLogger

from django.http import HttpRequest, HttpResponse

import time
import traceback

log = getLogger('all_requests')


SENSITIVE_HEADERS = [
    "HTTP_AUTHORIZATION",
    "HTTP_PROXY_AUTHORIZATION",
]


class LoggingRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest, *args, **kwargs):
        fields = self._get_request_fields(request)

        start_ns = time.perf_counter_ns()
        response = self.get_response(request, *args, **kwargs)
        end_ns = time.perf_counter_ns()

        total_ms = (end_ns - start_ns) / 1000
        response: HttpResponse

        fields.update(dict(total_ms=total_ms))
        fields.update(self._get_response_fields(response))
        if response.status_code != 200:
            fields.update(self._get_extra_request_fields(request))
            fields.update(self._get_extra_response_fields(response))

        level = logging.INFO
        if 500 <= response.status_code < 600:
            level = logging.ERROR
        if 400 <= response.status_code < 500:
            level = logging.WARNING

        msg = f''
        log.log(level, msg, extra=fields)

    def process_exception(self, request: HttpRequest, exception: Exception):
        tb_str = ''.join(traceback.format_exception(etype=type(exception), value=exception, tb=exception.__traceback__))

        return None

    def _get_request_fields(self, request: HttpRequest):
        return {}

    def _get_extra_request_fields(self, request: HttpRequest):
        headers = {
            f'req_{key}': value if key not in SENSITIVE_HEADERS else '******'
            for key, value in request.headers.items()
        }
        fields = dict(
            **headers,
            req_body=request.body.decode(errors='ignore'),
        )

        return fields

    def _get_extra_response_fields(self, response: HttpResponse):
        fields = dict(
            res_content=response.content.decode(errors='ignore'),
        )
        return fields

    def _get_response_fields(self, response: HttpResponse):
        fields = dict(
            res_status_code=response.status_code,
        )
        return fields

    def _gen_log_message_with_tb(self, request: HttpRequest, tb: str):
        pass
