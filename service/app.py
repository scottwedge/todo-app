from flask import Blueprint
from flask_restful import Api

from resources.task import TaskResource, TaskListResource
from resources.category import CategoryResource, CategoryListResource
from resources.user import User, UserRegister

service_blueprint = Blueprint("service", __name__)
service = Api(service_blueprint)


# Routes
service.add_resource(UserRegister, "/register")
service.add_resource(User, "/users/<int:user_id>")
service.add_resource(CategoryListResource, "/users/<int:user_id>/categories")
service.add_resource(CategoryResource, "/categories/<int:category_id>")
service.add_resource(TaskListResource, "/categories/<int:category_id>/tasks")
service.add_resource(TaskResource, "/tasks/<int:task_id>")
