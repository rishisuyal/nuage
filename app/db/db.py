from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv(".env")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
Base = declarative_base()
Session = sessionmaker(bind=engine)
db_session = Session()


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(45), nullable=False)
    full_name = Column(String(45), nullable=False)
    username = Column(String(45), nullable=False, unique=True)
    email = Column(String(45), nullable=False, unique=True)
    password = Column(String(45), nullable=False)
    submitted_by = Column(Integer)
    updated_at = Column(DateTime, default=datetime.now())

    students = relationship("Students", back_populates="user")
    attendance_logs = relationship("AttendanceLog", back_populates="user")
    departments = relationship("Departments", back_populates="user")
    courses = relationship("Courses", back_populates="user")


class Departments(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String(45), nullable=False)
    submitted_by = Column(Integer, ForeignKey("users.id"))
    updated_at = Column(DateTime, default=datetime.now())

    user = relationship("Users", back_populates="departments")
    students = relationship("Students", back_populates="department")
    courses = relationship("Courses", back_populates="department")


class Students(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(45), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    class_ = Column(String(45), nullable=False)
    submitted_by = Column(Integer, ForeignKey("users.id"))
    updated_at = Column(DateTime, default=datetime.now())

    user = relationship("Users", back_populates="students")
    department = relationship("Departments", back_populates="students")
    attendance_logs = relationship("AttendanceLog", back_populates="student")


class Courses(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(45), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    semester = Column(String(45), nullable=False)
    class_ = Column(String(45), nullable=False)
    lecture_hours = Column(Integer, nullable=False)
    submitted_by = Column(Integer, ForeignKey("users.id"))
    updated_at = Column(DateTime, default=datetime.now())

    user = relationship("Users", back_populates="courses")
    department = relationship("Departments", back_populates="courses")
    attendance_logs = relationship("AttendanceLog", back_populates="course")


class AttendanceLog(Base):
    __tablename__ = "attendance_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    present = Column(Boolean, nullable=False)
    submitted_by = Column(Integer, ForeignKey("users.id"))
    updated_at = Column(DateTime, default=datetime.now())

    student = relationship("Students", back_populates="attendance_logs")
    course = relationship("Courses", back_populates="attendance_logs")
    user = relationship("Users", back_populates="attendance_logs")


def create_schema():
    """
    Create the database schema if it does not exist.
    """
    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(engine)


def initialize():
    """
    Creates a user with the username 'vivek25' and password '4444'
    if no user exists in the database yet.
    """
    try:
        users_data = db_session.query(Users).first()
        if not users_data:
            insert_data = {
                "type": "admin",
                "full_name": "vivek",
                "username": "vivek25",
                "email": "test@test.com",
                "password": "4444",
            }
            obj = Users(**insert_data)
            db_session.add(obj)
            db_session.flush()
            db_session.commit()
            print("Password for username vivek25 is 4444")
    except Exception as e:
        db_session.rollback()
        print(f"Initialization error: {str(e)}")


create_schema()
initialize()
