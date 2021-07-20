def get_absolute_url(request, relative_path):
    scheme = request.scheme
    host = request.get_host()

    return f'{scheme}://{host}{relative_path}'
