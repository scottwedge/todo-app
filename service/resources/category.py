from flask import request
from flask_restful import Resource
from models.category import CategoryModel
from schemas.category import CategorySchema

category_schema = CategorySchema()
category_list_schema = CategorySchema(many=True)

# TODO: Use enum HttpStatusCode


class CategoryListResource(Resource):
    @classmethod
    def get(cls):
        return {"categories": category_list_schema.dump(CategoryModel.query.all())}, 200

    @classmethod
    def post(cls):
        json = request.get_json()
        category = category_schema.load(json)

        if CategoryModel.find_by_id(category.id):
            return {"message": "TODO"}, 400

        category.save_to_db()

        return category_schema.dump(category), 201


class CategoryResource(Resource):
    @classmethod
    def get(cls, category_id: int):
        category = CategoryModel.find_by_id(category_id)
        if category:
            return category_schema.dump(category), 200

        return {"message": "TODO, use seperate function for this!"}, 404
