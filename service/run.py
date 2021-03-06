from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from blacklist import BLACKLIST
from http_status_code import HttpStatusCode


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
jwt = JWTManager(app)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), HttpStatusCode.BAD_REQUEST.value


@jwt.expired_token_loader
def expired_token_callback(expired_token):
    token_type = expired_token["type"]
    return (
        jsonify(
            {
                "description": f"The {token_type} token has expired.",
                "error": "token_expired",
            }
        ),
        HttpStatusCode.UNAUTHORIZED.value,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify({"description": error, "error": "invalid_token"}),
        HttpStatusCode.UNPROCESSABLE_ENTITY.value,
    )


@jwt.unauthorized_loader
def unauthorized_loader_callback(error):
    return (
        jsonify({"description": error, "error": "missing_token"}),
        HttpStatusCode.UNAUTHORIZED.value,
    )


@jwt.token_in_blacklist_loader
def token_in_blacklist_callback(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST
