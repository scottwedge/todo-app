import os


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
# SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost/todo_app"
SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
JWT_SECRET_KEY = "2BFC39A71D9D581BFC1124F822D3E50C74DC6F002B9ABCF34A63A1157D954593"  # Not something you'd allow people to see in production
PROPAGATE_EXCEPTIONS = True  # TODO: Instead of this approach, override error handling in Flask-RESTful, see: https://github.com/vimalloc/flask-jwt-extended/issues/141#issuecomment-569524817
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
