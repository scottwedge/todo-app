from marshmallow_enum import EnumField

from ma import ma
from models.category import CategoryModel, Accent
from schemas.task import TaskSchema


class CategorySchema(ma.ModelSchema):
    tasks = ma.Nested(TaskSchema, many=True)
    accent = EnumField(Accent, by_value=True)

    class Meta:
        model = CategoryModel
        dump_only = ("id",)
        include_fk = True
