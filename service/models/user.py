from orm import orm


class UserModel(orm.Model):
    __tablename__ = "user"

    id = orm.Column(orm.Integer, primary_key=True)
    username = orm.Column(orm.String(64), unique=True, nullable=False)
    password = orm.Column(orm.String(94), nullable=False)

    categories = orm.relationship("CategoryModel", backref="user", lazy="dynamic")

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        orm.session.add(self)
        orm.session.commit()

    def delete_from_db(self) -> None:
        orm.session.delete(self)
        orm.session.commit()
