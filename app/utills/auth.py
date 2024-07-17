from functools import wraps
from flask import request, make_response, jsonify
from dotenv import load_dotenv
import jwt
import os
from datetime import datetime, timedelta
from .logger import Logger

load_dotenv(".env")
logger = Logger("auth").get()


def auth_decorator(func):
    """
    Decorator to authenticate API requests using JWT tokens.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The wrapped function with authentication logic.
    """

    @wraps(func)
    def inner():
        try:
            header = request.headers
            try:
                token = header["Authorization"].split(" ")[1]
            except Exception as e:
                logger.error(str({"msg": "Token Not Found! : ".upper() + str(e)}))
                return make_response(jsonify({"msg": "Token Not Found!"}), 401)
            secret_key = os.getenv("SECRET_KEY")
            decoded_str = jwt.decode(token, secret_key, ["HS256"])
            exp = datetime.strptime(decoded_str["expiration"], "%Y-%m-%d %H:%M:%S.%f")
            remains = datetime.now() - exp
            if remains > timedelta(seconds=120):
                logger.error(str({"msg": "Token Expired!"}))
                return make_response(jsonify({"msg": "Token Expired!"}), 401)
            # inner.__name__ = func.__name__
            return func()
        except Exception as e:
            logger.error(str({"msg": "Invalid Token! : ".upper() + str(e)}))
            return make_response(jsonify({"msg": "Invalid Token!"}), 401)

    return inner
