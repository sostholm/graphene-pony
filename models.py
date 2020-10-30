from __future__ import absolute_import, print_function, division

from pony.orm.core import *
from pony.orm.tests import db_params


db = Database()

class Student(db.Entity):
    _table_ = "Students"
    record = PrimaryKey(int)
    name = Required(unicode, column="fio")
    scholarship = Required(int, default=0)
    # marks = Set("Mark")

# class Mark(db.Entity):
#     _table_ = "Exams"
#     student = Required(Student, column="student")
#     value = Required(int)

db.bind(provider='sqlite', filename=':memory:')

db.generate_mapping(create_tables=True)


@db_session
def populate_db():


    s101 = Student(record=101, name='Bob', scholarship=0)
    s102 = Student(record=102, name='Joe', scholarship=800)
    s103 = Student(record=103, name='Alex', scholarship=0)
    s104 = Student(record=104, name='Brad', scholarship=500)
    s105 = Student(record=105, name='John', scholarship=1000)

    # Mark(student=s101, value=4)
    # Mark(student=s101, value=3)
    # Mark(student=s102, value=5)
    # Mark(student=s103, value=2)
    # Mark(student=s103, value=4)

populate_db()

# if __name__ == '__main__':
    # populate_db()