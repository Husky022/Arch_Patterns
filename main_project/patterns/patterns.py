import copy

class Prototype:

    def clone(self):
        return copy.deepcopy(self)

class Category:

    def __init__(self, name):
        self.name = name
        Engine.categories.append(self)


class Course(Prototype):

    def __init__(self, name, category, address):
        self.name = name
        self.category = category
        self.address = address
        self.lessons = []
        Engine.courses.append(self)

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


class User:
    def __init__(self, name, gender, birthday):
        self.name = name
        self.gender = gender
        self.birthday = birthday

class Student(User):
    pass

class Teacher(User):
    pass

class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create_user(cls, type, name, gender, birthday):
        return cls.types[type](name, gender, birthday)


class Engine:
    students = []
    teachers = []
    courses = []
    categories = []

    @staticmethod
    def create_user(type, name, gender, birthday):
        return UserFactory.create_user(type, name, gender, birthday)

    @staticmethod
    def create_category(name):
        return Category(name)

    @staticmethod
    def create_course(type, name, category, address):
        return CourseFactory.create_course(type, name, category, address)

