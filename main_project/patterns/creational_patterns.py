from abc import ABC, abstractmethod
import sqlite3
import copy
from patterns.behavioral_patterns import Notifier, Observable
from patterns.architectural_patterns import DomainObject


connection = sqlite3.connect('iqw_patterns.sqlite')

class Engine():

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

class Category(DomainObject):

    def __init__(self, name):
        self.name = name



class Course(Prototype, DomainObject):

    def __init__(self, name, category, address):

        self.name = name
        self.category = category
        self.address = address
        self.lessons = []
        self.teachers = []
        self.students = []

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

class Student(User, DomainObject):
    def __init__(self, name, gender, birthday):
        super().__init__(name, gender, birthday)

class Teacher(User, DomainObject):
    def __init__(self, name, gender, birthday):
        super().__init__(name, gender, birthday)

class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create_user(cls, type, name, gender, birthday):
        return cls.types[type](name, gender, birthday)

class UserMapper(ABC):
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def find_by_id(self):
        pass

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, gender, birthday) VALUES (?, ?, ?)"
        self.cursor.execute(statement, (obj.name, obj.gender, obj.birthday))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=?, SET gender=?, SET birthday=? WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
        self.cursor.execute(statement, (obj.name, obj.gender, obj.birthday, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class StudentMapper(UserMapper):

    def __init__(self, connection):
        super().__init__(connection)
        self.tablename = 'students'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, gender, birthday = item
            student = Student(name, gender, birthday)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT name, gender, birthday FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')


class TeacherMapper(UserMapper):

    def __init__(self, connection):
        super().__init__(connection)
        self.tablename = 'teachers'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, gender, birthday = item
            teacher = Teacher(name, gender, birthday)
            teacher.id = id
            result.append(teacher)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name, gender, birthday FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Teacher(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')


class CourseMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'courses'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, category, address, lessons, teachers, students = item
            course = Course(name, category, address)
            course.id = id
            result.append(course)
        return result

    def find_by_id(self, id):
        statement = f"SELECT name, category, address FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            course = Course(*result)
            course.id = id
            return course
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, category, address) VALUES (?, ?, ?)"
        self.cursor.execute(statement, (obj.name, obj.category, obj.address))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=?, SET category=?, SET address=? WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
        self.cursor.execute(statement, (obj.name, obj.category, obj.addressy, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CategoryMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'categories'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            category = Category(name)
            category.id = id
            result.append(category)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Category(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class MapperRegistry:
    mappers = {
        'students': StudentMapper,
        'teachers': TeacherMapper,
        'courses': CourseMapper,
        'categories': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)
        if isinstance(obj, Teacher):
            return TeacherMapper(connection)
        if isinstance(obj, Course):
            return CourseMapper(connection)
        if isinstance(obj, Category):
            return CategoryMapper(connection)


    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')

class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')



site = Engine()
notifier = Notifier()
observable = Observable()
