from models import *
from database import *
from schema import *
from service import *

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, status

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_database)):
    student = get_student_id(student_id, db)
    return student


@app.post("/enrollments", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_course(new_enrollment: EnrollmentCreate, db: Session = Depends(get_database)):
    enrollment = create_new_enrollment(
        student_id=new_enrollment.student_id, 
        course_id=new_enrollment.course_id, 
        db=db
    )
    return enrollment
