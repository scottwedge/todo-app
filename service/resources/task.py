from flask import request
from flask_restful import Resource
from models.task import TaskModel
from schemas.task import TaskSchema

task_schema = TaskSchema()
task_list_schema = TaskSchema(many=True)


class TaskListResource(Resource):
    @classmethod
    def get(cls):
        return {"tasks": task_list_schema.dump(TaskModel.query.all())}, 200

    @classmethod
    def post(cls):
        json = request.get_json()
        task = task_schema.load(json)

        task.save_to_db()

        return task_schema.dump(task), 201
