import sys, traceback
from django.http import JsonResponse

def error_response(code, message, status=400):
    return JsonResponse({
        'errors': [{
            'code': code,
            'message': message,
        }]
    }, status=status)


def print_traceback():
    type, value, tb = sys.exc_info()
    print(traceback.format_exception(type, value, tb))

def handler500(request):
    print_traceback()
    return error_response('unknown', 'Something went wrong. Please try again later.', status=500)

def handler400(request, exception):
    print_traceback()
    return error_response('unknown', 'Something went wrong. Please try again later.', status=400)

def handler404(request, exception):
    print_traceback()
    return error_response('notfound', 'Not found.', status=404)

def handler403(request, exception):
    print_traceback()
    return error_response('forbidden', 'You are not authorized to make this request.', status=403)
