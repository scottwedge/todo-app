from flask import request
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash, safe_str_cmp

from models.user import UserModel  # TODO: Check if this is redundant
from schemas.user import UserSchema
from http_status_code import HttpStatusCode

user_schema = UserSchema()

# Response messages
USER_ALREADY_EXISTS = "A user with that username already exists."
PASSWORD_TOO_SHORT = "Your password has to contain at least 8 characters."
USERNAME_TOO_LONG = "Username cannot be longer than 64 characters."
CREATED_SUCCESFULLY = "User created successfully."
USER_NOT_FOUND = "User not found."


def generate_message_json(message, http_status_code):
    return {"message": message}, http_status_code


class UserRegister(Resource):
    @classmethod
    def post(cls):
        json = request.get_json()
        user = user_schema.load(json)

        if UserModel.find_by_username(user.username):
            return generate_message_json(
                USER_ALREADY_EXISTS, HttpStatusCode.BAD_REQUEST.value
            )
        elif len(user.password) < 8:
            return generate_message_json(
                PASSWORD_TOO_SHORT, HttpStatusCode.BAD_REQUEST.value
            )

        # Hash password
        user.password = generate_password_hash(user.password)

        # Save user
        user.save_to_db()

        return generate_message_json(CREATED_SUCCESFULLY, HttpStatusCode.CREATED.value)


class User(Resource):
    """For testing purposes only"""

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return generate_message_json(USER_NOT_FOUND, HttpStatusCode.NOT_FOUND.value)

        return user_schema.dump(user), HttpStatusCode.OK.value

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return generate_message_json(USER_NOT_FOUND, HttpStatusCode.NOT_FOUND.value)

        user.delete_from_db()
        return HttpStatusCode.NO_CONTENT.value
