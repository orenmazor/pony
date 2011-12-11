import unittest
from pony.orm import *

db = Database('sqlite', ':memory:', create_db=True)

class Student(db.Entity):
    id = PrimaryKey(int)
    name = Required(unicode)
    group = Required('Group')
    ext_info = Optional('ExtInfo')

class ExtInfo(db.Entity):
    id = PrimaryKey(int)
    info = Required(unicode)
    student = Optional(Student)

class Group(db.Entity):
    number = PrimaryKey(int)
    students = Set(Student)

db.generate_mapping(create_tables=True)

g101 = Group(number=101)
g102 = Group(number=102)

s1 = Student(id=1, name='Student1', group=g101)
s2 = Student(id=2, name='Student2', group=g102)
ext_info = ExtInfo(id=100, info='ext_info1')
ext_info2 = ExtInfo(id=200, info='ext_info2')
commit()

class TestORMUndo(unittest.TestCase):
    def setUp(self):
        db.rollback()
    def test2(self):        
        try:
            Student[1].group = None
            self.assert_(False)
        except ConstraintError:
            self.assert_(True)
    def test3(self):
        try:
            Group[101].students = Group[102].students
            self.assert_(False)
        except ConstraintError:
            self.assert_(True)

if __name__ == '__main__':
    unittest.main()