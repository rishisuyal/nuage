from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from db.db import *
from utills import *
from datetime import timedelta, datetime
from dotenv import load_dotenv
import jwt
import os

app = Flask(__name__)
CORS(app)
logger = Logger().get()
load_dotenv(".env")


@app.route("/login", methods=["POST"])
def login():
    """
    Handle user login and generate a JWT token if credentials are valid.

    Returns:
        Response: JSON response with token or error message.
    """
    payload = request.json
    username = payload["username"]
    password = payload["password"]
    users_data = (
        db_session.query(Users)
        .filter(Users.username == username, Users.password == password)
        .first()
    )
    if not users_data:
        return make_response(jsonify({"msg": "username or password wrong!"}), 401)
    expiration = str(datetime.now() + timedelta(seconds=120))
    secret_key = os.getenv("SECRET_KEY")
    token = jwt.encode({"username": username, "expiration": expiration}, secret_key)
    return make_response(jsonify({"token": token}), 200)


@app.route("/attendance", methods=["POST", "GET"])
@auth_decorator
def attendance():
    """
    Handle attendance log operations (GET to fetch, POST to save).

    Returns:
        Response: JSON response with attendance data or error message.
    """
    try:
        ret_data = None
        if request.method == "GET":
            data = request.headers
            stu_id = data.get("stu_id")
            query_data = (
                db_session.query(Students)
                .join(AttendanceLog, Students.id == AttendanceLog.student_id)
                .filter(Students.id == stu_id)
                .all()
            )
            if not query_data:
                return make_response(jsonify({'msg' : 'Data Not Found!'}),404)
            ret_data = [orm_to_dict(i) for i in query_data]
        elif request.method == "POST":
            payload = request.json
            obj = AttendanceLog()
            ret_data = save(obj, payload)
        return make_response(jsonify({"data":ret_data}), 200)
    except Exception as e:
        db_session.rollback()
        logger.error(str(e))
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/courses", methods=["POST", "GET", "PATCH"])
@auth_decorator
def courses():
    """
    Handle course operations (GET to fetch, POST to save, PATCH to update).

    Returns:
        Response: JSON response with course data or error message.
    """
    try:
        ret_data = None
        if request.method == "GET":
            query_data = (
                db_session.query(Courses)
                .join(Departments, Departments.id == Courses.department_id)
                .all()
            )
            if not query_data:
                return make_response(jsonify({'msg' : 'Data Not Found!'}),404)
            ret_data = [orm_to_dict(i) for i in query_data]
        elif request.method == "POST":
            payload = request.json
            obj = Courses()
            ret_data = save(obj, payload)
        elif request.method == "PATCH":
            payload = request.json
            obj = (
                db_session.query(Courses)
                .filter(Courses.id == payload.pop("id"))
                .first()
            )
            ret_data = save(obj, payload)
        return make_response(jsonify({"data":ret_data}), 200)
    except Exception as e:
        db_session.rollback()
        logger.error(str(e))
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/students", methods=["POST", "GET", "PATCH"])
@auth_decorator
def students():
    """
    Handle student operations (GET to fetch, POST to save, PATCH to update).

    Returns:
        Response: JSON response with student data or error message.
    """
    try:
        ret_data = None
        if request.method == "GET":
            query_data = db_session.query(Students).all()
            if not query_data:
                return make_response(jsonify({'msg' : 'Data Not Found!'}),404)
            ret_data = [orm_to_dict(i) for i in query_data]
        elif request.method == "POST":
            payload = request.json
            obj = Students()
            ret_data = save(obj, payload)
        elif request.method == "PATCH":
            payload = request.json
            obj = (
                db_session.query(Students)
                .filter(Students.id == payload.pop("id"))
                .first()
            )
            ret_data = save(obj, payload)
        return make_response(jsonify({"data":ret_data}), 200)
    except Exception as e:
        db_session.rollback()
        logger.error(str(e))
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/department", methods=["POST", "GET", "PATCH"])
@auth_decorator
def department():
    """
    Handle department operations (GET to fetch, POST to save, PATCH to update).

    Returns:
        Response: JSON response with department data or error message.
    """
    try:
        ret_data = None
        if request.method == "GET":
            query_data = db_session.query(Departments).all()
            if not query_data:
                return make_response(jsonify({'msg' : 'Data Not Found!'}),404)
            ret_data = [orm_to_dict(i) for i in query_data]
        elif request.method == "POST":
            payload = request.json
            obj = Departments()
            ret_data = save(obj, payload)
        elif request.method == "PATCH":
            payload = request.json
            obj = (
                db_session.query(Departments)
                .filter(Departments.id == payload.pop("id"))
                .first()
            )
            ret_data = save(obj, payload)
        return make_response(jsonify({"data":ret_data}), 200)
    except Exception as e:
        db_session.rollback()
        logger.error(str(e))
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/users", methods=["POST", "GET", "PATCH"])
@auth_decorator
def users():
    """
    Handle user operations (GET to fetch, POST to save, PATCH to update).

    Returns:
        Response: JSON response with user data or error message.
    """
    try:
        ret_data = None
        if request.method == "GET":
            query_data = db_session.query(Users).all()
            if not query_data:
                return make_response(jsonify({'msg' : 'Data Not Found!'}),404)
            ret_data = [orm_to_dict(i) for i in query_data]
        elif request.method == "POST":
            payload = request.json
            obj = Users()
            ret_data = save(obj, payload)
        elif request.method == "PATCH":
            payload = request.json
            obj = db_session.query(Users).filter(Users.id == payload.pop("id")).first()
            ret_data = save(obj, payload)
        return make_response(jsonify({"data":ret_data}), 200)
    except Exception as e:
        db_session.rollback()
        logger.error(str(e))
        return make_response(jsonify({"error": str(e)}), 500)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
