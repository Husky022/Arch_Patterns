from iqw_framework.templator import render
from iqw_framework import logger
from patterns import patterns

site = patterns.Engine()
logger = logger.Logger('main')

def index(request):
    print(request)
    return '200 OK', render('index.html', data=request.get('secret', None))


def contacts(request):
    print(request)
    return '200 OK', render('contacts.html', data=request.get('key', None))

def registration(request):
    print(request)
    return '200 OK', render('registration.html', data=request.get('data', None))

def courses(request):
    print(request)
    return '200 OK', render('courses.html', courses_list=site.courses)

def course_redactor(request):
    print(request)
    return '200 OK', render('course_redactor.html', category_list=site.categories, courses_list=site.courses)

def not_found_404_view(request):
    print(request)
    return '404 WHAT', '404 PAGE Not Found'