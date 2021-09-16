from patterns.behavioral_patterns import LogToConsole, LogToFile


class SingletonLoggers(type):
   def __init__(cls, name, bases, attrs, **kwargs):
       super().__init__(name, bases, attrs)
       cls.logger_dict = {}
       cls.max_loggers = 2

   def __call__(cls, *args, **kwargs):
       name = args[0]
       if name not in cls.logger_dict.keys():
           if len(cls.logger_dict.keys()) == cls.max_loggers:
               raise ValueError("The maximum number of loggers is 2")
           cls.logger_dict[name] = super().__call__(*args, **kwargs)
       return cls.logger_dict[name]


class Logger(metaclass=SingletonLoggers):

    def __init__(self, name, strategy=LogToConsole()):
        self.name = name
        self.strategy = strategy

    def log(self, text):
        self.strategy.write(text)



