from database import Base
from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship


class DepartmentModel(Base):
    __tablename__ ='departments'

    id = Column(Integer,primary_key= True)
    name = Column(String(50),nullable= False)

    students= relationship('StudentModel', back_populates='department')

class StudentModel(Base):
    __tablename__='students'

    id=Column(Integer,primary_key=True)
    name = Column(String(50),nullable= False)
    status= Column(String(50),default='ACTIVE',nullable= False)
    department_id= Column(Integer,ForeignKey('departments.id'),nullable=False)

    department = relationship('DepartmentModel',back_populates='students')
    enrollments = relationship('EnrollmentModel',back_populates='student')

class CourseModel(Base):
    __tablename__ ='courses'

    id = Column(Integer,primary_key=True)
    name= Column(String(50),nullable= False)
    status= Column(String(50),default='OPEN',nullable=False)

    enrollments = relationship('EnrollmentModel',back_populates='course')


class EnrollmentModel(Base):
    __tablename__ ='enrollments'

    id= Column(Integer,primary_key=True)
    student_id = Column(Integer,ForeignKey('students.id'),nullable=False)
    course_id = Column(Integer,ForeignKey('courses.id'),nullable=False)

    student= relationship('StudentModel',back_populates='enrollments')
    course=relationship('CourseModel',back_populates='enrollments')
