from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_raw_jwt,
    jwt_refresh_token_required,
    jwt_required,
)
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash

from blacklist import BLACKLIST
from http_status_code import HttpStatusCode
from models.user import UserModel  # TODO: Check if this is redundant
from schemas.user import UserSchema
from util import generate_message_json

user_schema = UserSchema()

# Response messages
USER_ALREADY_EXISTS = "A user with that username already exists."
PASSWORD_TOO_SHORT = "Your password has to contain at least 8 characters."
USERNAME_TOO_LONG = "Username cannot be longer than 64 characters."
CREATED_SUCCESFULLY = "User created successfully."
USER_NOT_FOUND = "User not found."
INVALID_CREDENTIALS = "Invalid credentials."


class UserRegister(Resource):
    @classmethod
    def post(cls):
        json = request.get_json()
        user = user_schema.load(json)

        if UserModel.find_by_username(user.username):
            return generate_message_json(
                HttpStatusCode.BAD_REQUEST.value, USER_ALREADY_EXISTS
            )
        elif len(user.password) < 8:
            return generate_message_json(
                HttpStatusCode.BAD_REQUEST.value, PASSWORD_TOO_SHORT
            )

        # Hash password
        user.password = generate_password_hash(user.password)

        # Save user
        user.save_to_db()

        return generate_message_json(HttpStatusCode.CREATED.value, CREATED_SUCCESFULLY)


class UserLogin(Resource):
    @classmethod
    def post(cls):
        json = request.get_json()
        user = UserModel.find_by_username(json["username"])

        if user and check_password_hash(user.password, json["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return (
                {"access_token": access_token, "refresh_token": refresh_token},
                HttpStatusCode.OK.value,
            )

        return generate_message_json(
            HttpStatusCode.UNAUTHORIZED.value, INVALID_CREDENTIALS
        )


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        # JTI is the ID of the JWT
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        return generate_message_json(HttpStatusCode.OK.value, "Logged out.")


class User(Resource):
    """For testing purposes only"""

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return generate_message_json(HttpStatusCode.NOT_FOUND.value, USER_NOT_FOUND)

        return user_schema.dump(user), HttpStatusCode.OK.value

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return generate_message_json(HttpStatusCode.NOT_FOUND.value, USER_NOT_FOUND)

        user.delete_from_db()
        return "", HttpStatusCode.NO_CONTENT.value


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return generate_message_json(HttpStatusCode.OK.value, new_token, "access_token")
