from flask import Blueprint
from flask_restful import Api

from resources.task import TaskListResource

service_blueprint = Blueprint("service", __name__)
service = Api(service_blueprint)

service.add_resource(TaskListResource, "/tasks/")
