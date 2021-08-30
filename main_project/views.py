from iqw_framework.templator import render


def index(request):
    print(request)
    return '200 OK', render('index.html', data=request.get('secret', None))


def contacts(request):
    print(request)
    return '200 OK', render('contacts.html', data=request.get('key', None))

def registration(request):
    print(request)
    return '200 OK', render('registration.html', data=request.get('data', None))


def not_found_404_view(request):
    print(request)
    return '404 WHAT', '404 PAGE Not Found'