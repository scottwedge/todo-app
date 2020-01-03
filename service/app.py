from flask import Flask

from db import orm
from ma import ma
from views import service_blueprint

app = Flask(__name__)
# TODO: Switch to using a seperate config file
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route("/")
def test():
    return "Hello, World!"


@app.before_first_request
def create_tables():
    orm.create_all()


if __name__ == "__main__":
    orm.init_app(app)
    ma.init_app(app)
    app.register_blueprint(service_blueprint, url_prefix="/service")
    app.run(port=5000, debug=True)
