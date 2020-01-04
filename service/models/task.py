from orm import orm


class TaskModel(orm.Model):
    __tablename__ = "task"

    id = orm.Column(orm.Integer, primary_key=True)
    content = orm.Column(orm.String(120), nullable=False)

    def __init__(self, id, content):
        self.id = id
        self.content = content
