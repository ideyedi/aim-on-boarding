from flask import Blueprint, jsonify, Flask, url_for
from flask_swagger_ui import get_swaggerui_blueprint

from app.view.user import UserView
from config import DevelopConfig

route_bp = Blueprint("route", __name__)


def route_extension(app: Flask):
    UserView.register(route_bp, route_base="/user")
    # apispec 생성
    register_swagger(route_bp)
    app.register_blueprint(route_bp)

    # swagger-ui
    swagger_bp = get_swaggerui_blueprint(
        DevelopConfig.APISPEC_SWAGGER_UI_URL,
        "/apispec",
    )
    app.register_blueprint(swagger_bp)


def register_swagger(bp: Blueprint):
    """
    apispec generator
    """
    from core import generate_api_spec

    @bp.route("/apispec")
    def apispec():
        return jsonify(generate_api_spec(title="on-boarding",
                                         version="v1",
                                         bp_name=bp.name if isinstance(bp, Blueprint) else None
                                         )
                       )
