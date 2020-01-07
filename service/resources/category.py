from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from util import generate_message_json, check_attr
from http_status_code import HttpStatusCode
from models.category import CategoryModel
from schemas.category import CategorySchema

category_schema = CategorySchema()
category_list_schema = CategorySchema(many=True)

# Response messages
CATEGORY_ALREADY_EXISTS = "A category with that name already exists."
CATEGORY_NOT_FOUND = "Category not found."
FIELD_CANNOT_BE_EDITED = "The {} cannot be edited."
INVALID_ATTR = "Invalid attributes and/or invalid values for specfied attrubutes."


class CategoryListResource(Resource):
    @classmethod
    @jwt_required
    def get(cls, user_id: int):
        return generate_message_json(
            HttpStatusCode.OK.value,
            category_list_schema.dump(CategoryModel.query.filter_by(user_id=user_id)),
            "categories",
        )

    @classmethod
    @jwt_required
    def post(cls, user_id: int):
        json = request.get_json()
        json["user_id"] = user_id
        category = category_schema.load(json)

        if CategoryModel.find_by_user_id_and_title(category.user_id, category.title):
            return generate_message_json(
                HttpStatusCode.BAD_REQUEST.value, CATEGORY_ALREADY_EXISTS
            )

        category.save_to_db()

        return category_schema.dump(category), HttpStatusCode.CREATED.value


class CategoryResource(Resource):
    @classmethod
    @jwt_required
    def get(cls, category_id: int):
        category = CategoryModel.find_by_id(category_id)
        if category:
            return category_schema.dump(category), HttpStatusCode.OK.value

        return generate_message_json(HttpStatusCode.NOT_FOUND.value, CATEGORY_NOT_FOUND)

    @classmethod
    @jwt_required
    def patch(cls, category_id: int):
        json = request.get_json()

        # Check if the category exists
        category = CategoryModel.find_by_id(category_id)
        if not category:
            return generate_message_json(
                HttpStatusCode.NOT_FOUND.value, CATEGORY_NOT_FOUND
            )

        # Check if client is trying to edit readonly fields
        readonly = {"id", "user_id", "tasks"}
        keys = json.keys()
        forbidden = readonly & keys

        if forbidden:
            return generate_message_json(
                HttpStatusCode.BAD_REQUEST.value,
                FIELD_CANNOT_BE_EDITED.format(str(forbidden)[1:-1]),
            )

        # Check if the client specified non existing attrs

        try:
            check_attr(json.keys(), category)
            for key, value in json.items():
                setattr(category, key, value)

            category.save_to_db()
            return category_schema.dump(category), HttpStatusCode.OK.value
        except AttributeError as ae:
            return generate_message_json(HttpStatusCode.BAD_REQUEST.value, str(ae))
        except SQLAlchemyError as se:
            return generate_message_json(HttpStatusCode.BAD_REQUEST.value, str(se))

    @classmethod
    @jwt_required
    def delete(cls, category_id: int):
        category = CategoryModel.find_by_id(category_id)
        if category:
            # NOTE: Deletion will currently fail if the category contains any tasks
            category.delete_from_db()
            return "", HttpStatusCode.NO_CONTENT.value

        return generate_message_json(HttpStatusCode.NOT_FOUND.value, CATEGORY_NOT_FOUND)
