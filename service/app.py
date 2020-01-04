from flask import Blueprint
from flask_restful import Api

from resources.task import TaskListResource
from resources.user import User, UserRegister

service_blueprint = Blueprint("service", __name__)
service = Api(service_blueprint)


# Routes
service.add_resource(UserRegister, "/register")
service.add_resource(TaskListResource, "/tasks")
service.add_resource(User, "/users/<int:user_id>")
