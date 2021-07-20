DEFAULT_LIST_LIMIT = 20
DEFAULT_LIST_OFFSET = 0

def paginate(queryset, limit=DEFAULT_LIST_LIMIT, offset=DEFAULT_LIST_OFFSET) -> tuple(list, int):
    return list(queryset[offset:offset+limit]), queryset.count()
