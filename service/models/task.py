from orm import orm
from enum import Enum
from typing import List


class Priority(Enum):
    DEFAULT = 0
    LOW = 1
    MEDIUM = 2
    TOP = 3


class TaskModel(orm.Model):
    __tablename__ = "task"

    id = orm.Column(orm.Integer, primary_key=True)
    content = orm.Column(orm.String(120), nullable=False)
    note = orm.Column(orm.String(255))
    priority = orm.Column(orm.Enum(Priority), nullable=False)
    due_date = orm.Column(orm.TIMESTAMP)
    completed = orm.Column(orm.Boolean, nullable=False)

    category_id = orm.Column(orm.Integer, orm.ForeignKey("category.id"), nullable=False)

    @classmethod
    def find_by_id(cls, _id: int) -> "TaskModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls, priority: Priority = None) -> List["TaskModel"]:
        if not priority:
            return cls.query.all()
        else:
            return cls.query.filter_by(priority=priority.value)

    def save_to_db(self) -> None:
        orm.session.add(self)
        orm.session.commit()

    def delete_from_db(self) -> None:
        orm.session.delete(self)
        orm.session.commit()
