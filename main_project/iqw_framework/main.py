import quopri
from wsgiref.util import setup_testing_defaults
import views
from datetime import datetime


class Framework():
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        setup_testing_defaults(environ)
        print(environ)
        path = environ['PATH_INFO']
        if path == '/index.html':
            path ='/'
        if path.endswith('.html'):
            path = path.rstrip('.html')
        if not path.endswith('/'):
            path += '/'

        request = {}

        method = environ['REQUEST_METHOD']
        if method == 'GET':
            #Добавил здесь просто вывод данных в терминал, могу также добавить вывод в файл, если требуется
            print(f'{datetime.now()} - GET запрос, данные запроса - {self.handler_data(environ["QUERY_STRING"])}')
        if method == 'POST':
            #Также, вывод в терминал
            data_from_post = self.wsgi_input_data(environ)
            print(f'{datetime.now()} - POST запрос, данные запроса - {self.data_decoder(data_from_post)}')


        if path in self.routes:
            view = self.routes[path]
        else:
            view = views.not_found_404_view
        for front in self.fronts:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]


    def handler_data(self, data):
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result


    def wsgi_input_data(self, env):
        content_length_data = env['CONTENT_LENGTH']
        content_length = int(content_length_data)
        data = env['wsgi.input'].read(content_length)
        return data


    def data_decoder(self, data):
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            handling_data = self.handler_data(data_str)
            for k, v in handling_data.items():
                val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
                val_decode_str = quopri.decodestring(val).decode('UTF-8')
                result[k] = val_decode_str
        return result

