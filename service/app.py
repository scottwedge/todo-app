from flask import Blueprint
from flask_restful import Api as _Api

from resources.category import CategoryListResource, CategoryResource
from resources.task import TaskListResource, TaskResource
from resources.user import TokenRefresh, User, UserLogin, UserLogout, UserRegister

CUSTOM_ERRORS = dict()  # NOTE: This dict should contain any and all custom errors


class Api(_Api):
    def error_router(self, original_handler, e):
        """ Override original error_router to only custom errors and parsing error (from webargs)"""

        # extract the error class name as a string
        error_type = type(e).__name__.split(".")[-1]
        # if error can be handled by flask_restful's Api object, do so
        # otherwise, let Flask handle the error
        # the 'UnprocessableEntity' is included only because I'm also using webargs
        # feel free to omit it
        if self._has_fr_route() and error_type in list(CUSTOM_ERRORS) + [
            "UnprocessableEntity"
        ]:
            try:
                return self.handle_error(e)
            except Exception:
                pass  # Fall through to original handler

        return original_handler(e)


service_blueprint = Blueprint("service", __name__)
service = Api(service_blueprint)


# Routes
service.add_resource(UserRegister, "/register")
service.add_resource(UserLogin, "/login")
service.add_resource(UserLogout, "/logout")
service.add_resource(TokenRefresh, "/refresh")
service.add_resource(User, "/users/<int:user_id>")
service.add_resource(CategoryListResource, "/users/<int:user_id>/categories")
service.add_resource(CategoryResource, "/categories/<int:category_id>")
service.add_resource(TaskListResource, "/categories/<int:category_id>/tasks")
service.add_resource(TaskResource, "/tasks/<int:task_id>")
