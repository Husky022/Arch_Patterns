from wsgiref.simple_server import make_server
from application.urls import routes, fronts
from application.model import Application

application = Application(routes, fronts)

if __name__ == "__main__":
    with make_server('', 8000, application) as httpd:
        print("Server is running on port 8000...")
        httpd.serve_forever()