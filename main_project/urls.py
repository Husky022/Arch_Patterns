import views


def secret_front(request):
    request['secret'] = 'some secret'


def other_front(request):
    request['key'] = 'key'


routes = {
    '/': views.index,
    '/contacts/': views.contacts,
    '/registration/': views.registration,
    '/courses/': views.courses,
    '/course_redactor/': views.course_redactor
}

fronts = [secret_front, other_front]

