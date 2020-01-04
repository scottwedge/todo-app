from ma import ma
from models.user import UserModel
from schemas.category import CategorySchema


class UserSchema(ma.ModelSchema):
    categories = ma.Nested(CategorySchema, many=True)

    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
