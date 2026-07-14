from models import *
from sqlalchemy.orm import Session
from fastapi import HTTPException

def get_student_id(id: int, db: Session):
    student = db.query(StudentModel).filter(StudentModel.id == id).first()
    
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    
    course_list = [enrollment.course for enrollment in student.enrollments]
    
    return {
        "id": student.id,
        "name": student.name,
        "status": student.status,
        "department": student.department,
        "enrollments": course_list
    }


def create_new_enrollment(student_id: int, course_id: int, db: Session):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=400,
            detail="Sinh viên không tồn tại")
        
    if student.status != "ACTIVE":
        raise HTTPException(
            status_code=400, 
            detail="Sinh viên không ở trạng thái ACTIVE"
        )

    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=400,
            detail="Khóa học không tồn tại"
        )
        
    if course.status != "OPEN":
        raise HTTPException(
            status_code=400,
            detail="Khóa học đã đóng, không thể đăng ký"
        )

    is_duplicated = db.query(EnrollmentModel).filter(
        EnrollmentModel.student_id == student_id,
        EnrollmentModel.course_id == course_id
    ).first()
    if is_duplicated:
        raise HTTPException(
            status_code=400,
            detail="Sinh viên đã đăng ký khóa học này rồi"
        )

    new_enrollment = EnrollmentModel(student_id=student_id, course_id=course_id)
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    
    return new_enrollment
