DEFAULT_LIST_LIMIT = 20

def paginate(queryset, request):
    try:
        limit = int(request.GET.get('limit'))
    except:
        limit = DEFAULT_LIST_LIMIT
    try:
        offset = int(request.GET.get('offset'))
    except:
        offset = 0

    return queryset[offset:offset+limit]
