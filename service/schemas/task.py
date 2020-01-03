from ma import ma
from models.task import TaskModel


class TaskSchema(ma.ModelSchema):
    class Meta:
        model = TaskModel
        dump_only = ("id",)
