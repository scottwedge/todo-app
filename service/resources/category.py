from flask import request
from flask_restful import Resource

from util import generate_message_json
from http_status_code import HttpStatusCode
from models.category import CategoryModel
from schemas.category import CategorySchema

category_schema = CategorySchema()
category_list_schema = CategorySchema(many=True)

# Response messages
CATEGORY_ALREADY_EXISTS = "A category with that name already exists."
CATEGORY_NOT_FOUND = "Category not found."


class CategoryListResource(Resource):
    @classmethod
    def get(cls, user_id: int):
        return generate_message_json(
            HttpStatusCode.OK.value,
            category_list_schema.dump(CategoryModel.query.filter_by(user_id=user_id)),
            "categories",
        )

    @classmethod
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
    def get(cls, category_id: int):
        category = CategoryModel.find_by_id(category_id)
        if category:
            return category_schema.dump(category), HttpStatusCode.OK.value

        return generate_message_json(HttpStatusCode.NOT_FOUND.value, CATEGORY_NOT_FOUND)

    @classmethod
    def delete(cls, category_id: int):
        category = CategoryModel.find_by_id(category_id)
        if category:
            # NOTE: Deletion will currently fail if the category contains any tasks
            category.delete_from_db()
            return "", HttpStatusCode.NO_CONTENT.value

        return generate_message_json(HttpStatusCode.NOT_FOUND.value, CATEGORY_NOT_FOUND)
