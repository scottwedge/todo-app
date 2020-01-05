from flask import request
from flask_restful import Resource

from util import generate_message_json
from http_status_code import HttpStatusCode
from models.task import TaskModel
from schemas.task import TaskSchema

task_schema = TaskSchema()
task_list_schema = TaskSchema(many=True)

# Response message
TASK_NOT_FOUND = "Task not found."


class TaskListResource(Resource):
    @classmethod
    def get(cls, category_id: int):
        return generate_message_json(
            HttpStatusCode.OK.value,
            task_list_schema.dump(TaskModel.query.filter_by(category_id=category_id)),
            "tasks",
        )

    @classmethod
    def post(cls, category_id: int):
        json = request.get_json()
        json["category_id"] = category_id
        task = task_schema.load(json)

        task.save_to_db()

        return task_schema.dump(task), HttpStatusCode.CREATED.value


class TaskResource(Resource):
    @classmethod
    def get(cls, task_id: int):
        task = TaskModel.find_by_id(task_id)
        if task:
            return task_schema.dump(task), HttpStatusCode.OK.value

        return generate_message_json(HttpStatusCode.NOT_FOUND.value, TASK_NOT_FOUND)

    @classmethod
    def delete(cls, task_id: int):
        task = TaskModel.find_by_id(task_id)
        if task:
            task.delete_from_db()
            return "", HttpStatusCode.NO_CONTENT.value

        return generate_message_json(HttpStatusCode.NOT_FOUND.value, TASK_NOT_FOUND)
