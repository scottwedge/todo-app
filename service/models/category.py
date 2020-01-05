from orm import orm
from enum import Enum
from typing import List


class Accent(Enum):
    BLACK = "BLACK"
    BLUE = "BLUE"
    BROWN = "BROWN"
    GOLD = "GOLD"
    GRAY = "GRAY"
    GREEN = "GREEN"
    ORANGE = "ORANGE"
    PURPLE = "PURPLE"


class CategoryModel(orm.Model):
    __tablename__ = "category"

    id = orm.Column(orm.Integer, primary_key=True)
    title = orm.Column(orm.String(40), nullable=False)
    accent = orm.Column(orm.Enum(Accent), nullable=False, server_default=("BLUE"))

    tasks = orm.relationship("TaskModel", backref="category", lazy="dynamic")

    user_id = orm.Column(orm.Integer, orm.ForeignKey("user.id"), nullable=False)

    @classmethod
    def find_by_id(cls, _id: int) -> "CategoryModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_user_id_and_title(cls, user_id: int, title: str) -> "CategoryModel":
        return cls.query.filter_by(user_id=user_id, title=title).first()

    @classmethod
    def find_all(cls) -> List["CategoryModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        orm.session.add(self)
        orm.session.commit()

    def delete_from_db(self) -> None:
        orm.session.delete(self)
        orm.session.commit()
