from wsgiref.simple_server import make_server
from urls import fronts
from views import routes
from iqw_framework.main import Framework, LogFramework, FakeFramework

application = Framework(routes, fronts)

if __name__ == "__main__":
    with make_server('', 8000, application) as httpd:
        print("Server is running on port 8000...")
        httpd.serve_forever ()