import abc
from datetime import datetime
import json


# паттерн для Логера - Стратегия
from patterns.architectural_patterns import DomainObject


class LogToConsole:

    def write(self, text):
        print(f"{datetime.now()}: ---- {text} \n")


class LogToFile:

    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, text):
        text = f"{datetime.now()}: ---- {text} \n"
        with open(self.file_name +"_log.txt", "a") as file:
            file.write(f"{datetime.now()}: ---- {text} \n")


# api курсов
class Api:

    def __init__(self, object):
        self.object = object

    def convert_to_json(self):
        object_list = []
        result = {}
        for item in self.object:
                dict_item = {property: item.__dict__[property] for property in item.__dict__.keys()}
                object_list.append(dict_item)
        result[f'Доступные курсы на {datetime.today().strftime("%d.%m.%Y")}'] = object_list
        return json.dumps(result, ensure_ascii=False, sort_keys=True, indent=4)


# паттерн Наблюдатель
class Observer(metaclass=abc.ABCMeta):
   def __init__(self):
       self._subject = None
       self._observer_state = None

   @abc.abstractmethod
   def update(self, course_name):
       pass


class Notifier(Observer):
    def update(self, course_name, user_name):
        print(f'Отправлено SMS пользователю {user_name}: Добавлен курс {course_name} ')
        print(f'Отправлено письмо по email пользователю {user_name}: Добавлен курс {course_name} ')

class Observable:

   def notify(self, name, observer):
       observer.update(name, observer.name)