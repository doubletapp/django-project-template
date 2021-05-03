import json
from django.test import RequestFactory


request_factory = RequestFactory()


def get_json_request(request_method, **kwargs):
    request_kwargs = {
        'content_type': 'application/json',
        'path': None,
        **kwargs,
    }
    return getattr(request_factory, request_method)(**request_kwargs)


def get_json_response(view, request, **kwargs):
    response = view.as_view()(request, **kwargs)
    response.data = json.loads(response.content)
    return response
