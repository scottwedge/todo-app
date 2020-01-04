from marshmallow_enum import EnumField

from ma import ma
from models.task import TaskModel, Priority


class TaskSchema(ma.ModelSchema):
    priority = EnumField(Priority, by_value=True)

    class Meta:
        model = TaskModel
        dump_only = ("id",)
        include_fk = True
