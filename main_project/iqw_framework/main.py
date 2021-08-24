from wsgiref.util import setup_testing_defaults
import views


class Framework():
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        setup_testing_defaults(environ)
        print(environ)
        print('work')
        path = environ['PATH_INFO']
        if not path.endswith('/'):
            path += '/'
        request = {}
        if path in self.routes:
            view = self.routes[path]
        else:
            view = views.not_found_404_view
        for front in self.fronts:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]