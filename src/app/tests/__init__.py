import json
from django.test import RequestFactory
from django.http import JsonResponse, HttpRequest


request_factory = RequestFactory()


def get_json_request(request_method, **kwargs) -> HttpRequest:
    request_kwargs = {
        'content_type': 'application/json',
        'path': None,
        **kwargs,
    }
    return getattr(request_factory, request_method)(**request_kwargs)


def get_json_response(view, request, **kwargs) -> JsonResponse:
    response = view.as_view()(request, **kwargs)
    response.data = json.loads(response.content)
    return response
