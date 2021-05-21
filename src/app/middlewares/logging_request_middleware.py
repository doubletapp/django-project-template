import logging
from logging import getLogger

from django.http import HttpRequest, HttpResponse

import time
import traceback


def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
    """
    A factory method which can be overridden in subclasses to create
    specialized LogRecords.
    """
    rv = logging.LogRecord(name, level, fn, lno, msg, args, exc_info, func, sinfo)
    if extra is not None:
        rv.__dict__.update(extra)
    return rv


log = getLogger('app')
log.__class__.makeRecord = makeRecord

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
        fields.update(dict(total_ms=total_ms))
        fields.update(self._get_response_fields(response))
        if response.status_code != 200:
            fields.update(self._get_extra_request_fields(request))
            fields.update(self._get_extra_response_fields(response))

        level = logging.INFO
        if 500 <= response.status_code < 600:
            level = logging.CRITICAL
        if 400 <= response.status_code < 500:
            level = logging.ERROR

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

        if response.status_code == 500 and hasattr(request, 'exc_info'):
            ex = getattr(request, 'exc_info')
            tb_str = ''.join(traceback.format_exception(type(ex), ex, ex.__traceback__))
            msg += f'\n{tb_str}'
            fields.update(dict(
                traceback=tb_str,
                **self._get_path_and_line_of_exc(ex)
            ))

        log.log(level, msg, extra=fields)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        request.exc_info = exception

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

    def _get_path_and_line_of_exc(self, ex):
        tb = self._get_last_tb_obj(ex.__traceback__)
        pathname = tb.tb_frame.f_code.co_filename
        lineno = tb.tb_lineno

        return dict(
            pathname=pathname,
            lineno=lineno,
        )

    def _get_last_tb_obj(self, tb):
        cur = tb
        while cur.tb_next is not None:
            cur = cur.tb_next

        return cur
