import views


def secret_front(request):
    request['secret'] = 'some secret'


def other_front(request):
    request['key'] = 'key'


routes = {
    '/': views.index,
    '/contacts/': views.contacts,
    '/registration/': views.registration
}

fronts = [secret_front, other_front]

