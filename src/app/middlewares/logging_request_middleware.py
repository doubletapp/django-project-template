import logging
from logging import getLogger

from django.http import HttpRequest, HttpResponse

import time
import traceback

log = getLogger('app')


SENSITIVE_HEADERS = [
    "Authorization",
    "Proxy-Authorization",
]


class LoggingRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest, *args, **kwargs):
        fields = self._get_request_fields(request)

        start_ns = time.perf_counter_ns()
        response = self.get_response(request, *args, **kwargs)
        end_ns = time.perf_counter_ns()

        total_ms = (end_ns - start_ns) / 1e6
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

        msg = f'[{total_ms:.3f} ms] {request.method} {request.path} {response.status_code}'
        if response.status_code != 200:
            to_log = dict(
                **self._get_request_headers(request),
                body=request.body.decode(errors='ignore')
            )
            msg += '\n' + '\n'.join(
                f'{key}: {value}'
                for key, value in to_log.items()
            )

        if response.status_code == 500:
            msg += '\nTHIS IS TRACEBACK'

        log.log(level, msg, extra=fields)
        return response

    # def process_exception(self, request: HttpRequest, exception: Exception):
    #     tb_str = ''.join(traceback.format_exception(etype=type(exception), value=exception, tb=exception.__traceback__))

    def _get_request_fields(self, request: HttpRequest):
        return {}

    def _get_extra_request_fields(self, request: HttpRequest):
        headers = {f'req_{key}': value for key, value in self._get_request_headers(request).items()}
        fields = dict(
            **headers,
            req_body=request.body.decode(errors='ignore'),
        )

        return fields

    def _get_request_headers(self, request: HttpRequest):
        return {
            key: value if key not in SENSITIVE_HEADERS else '******'
            for key, value in request.headers.items()
        }

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
