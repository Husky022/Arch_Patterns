from jinja2 import FileSystemLoader
from jinja2 import Environment


def render(template_name, folder='templates', **kwargs):
   env = Environment()
   # указываем папку для поиска шаблонов
   env.loader = FileSystemLoader(folder)
   # находим шаблон в окружении
   template = env.get_template(template_name)
   return template.render(**kwargs)
