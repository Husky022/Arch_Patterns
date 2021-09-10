
class AppRoute:

    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, func):
        self.routes[self.url] = func

class Debug:

    def __init__(self, name):

        self.name = name

    def __call__(self, func):

        def benchmark(func):
            from time import time
            def wrapper(*args, **kw):
                start = time()
                ret_val = func(*args, **kw)
                end = time()
                res = start - end

                print(f'Время выполнения {self.name} = {res} ms')
                return ret_val

            return wrapper

        return benchmark(func)
