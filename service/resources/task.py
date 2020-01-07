from flask import request
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from util import generate_message_json, check_attr
from http_status_code import HttpStatusCode
from models.task import TaskModel
from schemas.task import TaskSchema

task_schema = TaskSchema()
task_list_schema = TaskSchema(many=True)

# Response message
TASK_NOT_FOUND = "Task not found."
FIELD_CANNOT_BE_EDITED = "The {} cannot be edited."
INVALID_ATTR = "Invalid attributes and/or invalid values for specfied attrubutes."


class TaskListResource(Resource):
    @classmethod
    @jwt_required
    def get(cls, category_id: int):
        return generate_message_json(
            HttpStatusCode.OK.value,
            task_list_schema.dump(TaskModel.query.filter_by(category_id=category_id)),
            "tasks",
        )

    @classmethod
    @jwt_required
    def post(cls, category_id: int):
        json = request.get_json()
        json["category_id"] = category_id
        task = task_schema.load(json)

        task.save_to_db()

        return task_schema.dump(task), HttpStatusCode.CREATED.value


class TaskResource(Resource):
    @classmethod
    @jwt_required
    def get(cls, task_id: int):
        task = TaskModel.find_by_id(task_id)
        if task:
            return task_schema.dump(task), HttpStatusCode.OK.value

        return generate_message_json(HttpStatusCode.NOT_FOUND.value, TASK_NOT_FOUND)

    @classmethod
    @jwt_required
    def patch(cls, task_id: int):
        json = request.get_json()

        # Check if the task exists
        task = TaskModel.find_by_id(task_id)
        if not task:
            return generate_message_json(HttpStatusCode.NOT_FOUND.value, TASK_NOT_FOUND)

        # Check if client is trying to edit readonly fields
        readonly = {"id", "category_id"}
        keys = json.keys()
        forbidden = readonly & keys

        if forbidden:
            return generate_message_json(
                HttpStatusCode.BAD_REQUEST.value,
                FIELD_CANNOT_BE_EDITED.format(str(forbidden)[1:-1]),
            )

        # Check if the client specified non existing attrs

        if check_attr(json.keys(), task):
            try:
                for key, value in json.items():
                    setattr(task, key, value)

                task.save_to_db()  # Persist chages to db
            except SQLAlchemyError:
                # NOTE: This isn't a good error message in that it lacks proper information
                return generate_message_json(
                    HttpStatusCode.BAD_REQUEST.value, INVALID_ATTR
                )

            return task_schema.dump(task), HttpStatusCode.OK.value

        return generate_message_json(HttpStatusCode.BAD_REQUEST.value, INVALID_ATTR)

    @classmethod
    @jwt_required
    def delete(cls, task_id: int):
        task = TaskModel.find_by_id(task_id)
        if task:
            task.delete_from_db()
            return "", HttpStatusCode.NO_CONTENT.value

        return generate_message_json(HttpStatusCode.NOT_FOUND.value, TASK_NOT_FOUND)
