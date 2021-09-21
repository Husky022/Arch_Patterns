



class Course():

    id = 0


    def __init__(self):
        Course.id += 1



ar_1 = Course()
ar_2 = Course()
ar_3 = Course()
print(ar_1.id)
print(ar_2.id)
print(ar_3.id)