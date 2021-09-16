import copy
from patterns.behavioral_patterns import Subject, Notifier


class Engine():
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type, name, gender, birthday):
        return UserFactory.create_user(type, name, gender, birthday)

    @staticmethod
    def create_category(name):
        return Category(name)

    @staticmethod
    def create_course(type, name, category, address):
        return CourseFactory.create_course(type, name, category, address)


class Prototype:

    def clone(self):
        return copy.deepcopy(self)

class Category:

    def __init__(self, name):
        self.name = name
        site.categories.append(self)


class Course(Prototype):

    def __init__(self, name, category, address):
        self.name = name
        self.category = category
        self.address = address
        self.lessons = []
        self.teachers = []
        self.students = []
        site.courses.append(self)
        observable.notify(self.name)


class OfflineCourse(Course):
    def __init__(self, name, category, address):
        super().__init__(name, category, address)
        self.type = 'offline'

class OnlineCourse(Course):
    def __init__(self, name, category, address):
        super().__init__(name, category, address)
        self.type = 'online'

class CourseFactory:
    types = {
        'online': OnlineCourse,
        'offline': OfflineCourse
    }

    @classmethod
    def create_course(cls, type, name, category, address):
        return cls.types[type](name, category, address)


class User(Notifier):
    def __init__(self, name, gender, birthday):
        super().__init__()
        self.name = name
        self.gender = gender
        self.birthday = birthday

class Student(User):
    def __init__(self, name, gender, birthday):
        super().__init__(name, gender, birthday)
        site.students.append(self)
        observable.attach(self)
        print(f'список студентов - {site.students}')

class Teacher(User):
    def __init__(self, name, gender, birthday):
        super().__init__(name, gender, birthday)
        site.teachers.append(self)
        print(f'список преподов - {site.teachers}')

class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create_user(cls, type, name, gender, birthday):
        return cls.types[type](name, gender, birthday)


site = Engine()
observable = Subject()
notifier = Notifier()