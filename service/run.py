from flask import Flask


def create_app(confif_filename):
    app = Flask(__name__)
    app.config.from_object(confif_filename)

    from app import service_blueprint

    app.register_blueprint(service_blueprint, url_prefix="/service")

    from orm import orm

    orm.init_app(app)

    from ma import ma

    ma.init_app(app)

    from flask_migrate import Migrate

    migrate = Migrate(app, orm)

    return app


# TODO: Catch and handle marshmallow exceptions

app = create_app("config")
