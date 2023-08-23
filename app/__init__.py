import mongoengine as me
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from flask_api import status

from app.view.user import UserView
from app.view import route_extension
from config import DevelopConfig


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")

    app.config.update({"APISPEC_SPEC": DevelopConfig.APISPEC_SPEC,
                       "APISPEC_SWAGGER_URL": DevelopConfig.APISPEC_SWAGGER_URL,
                       "APISPEC_SWAGGER_UI_URL": DevelopConfig.APISPEC_SWAGGER_UI_URL
                       })

    app.config["DOC_TITLE"] = "Swagger-Classful"
    app.config["DOC_VERSION"] = "0.0.1"
    app.config["DOC_OPEN_API_VERSION"] = "3.0.2"

    CORS(send_wildcard=True,
         resources={r'*': {'origins': '*'}},
         expose_headers=["content-disposition"],
         max_age=6000).init_app(app)
    #
    register_db()
    #UserView.register(app, route_base="/user")
    route_extension(app)

    print(app.url_map)

    @app.route("/actuator")
    def heath_check():
        """
        Health Check Endpoint
        """
        return ("OK",
                status.HTTP_200_OK)

    return app


def register_db():
    """
    MongoEngine 셋업
    :return:
    """
    try:
        me.connect(host=DevelopConfig.mongo_url)
    except ConnectionError:
        print(f"{str(ConnectionError)}")
    except Exception as e:
        print(f"{str(e)}")


def register_apidocs(bp, title="On-boarding", version="v0.0.1"):
    global_params = [{"description": "호스트 언어(ko, en, vi, ja)", "in": "query", "name": "hl", "schema": {"type": "string"}}, {"description": "국가(kr, us, vn, jp)", "in": "query", "name": "cr", "schema": {"type": "string"}}]

    print(__name__)
    from core import generate_api_spec
    from flask import render_template, url_for

    def get_api_spec_url():
        if isinstance(bp, Blueprint):
            return url_for(f"{bp.name}.apispec")
        else:
            return url_for("apispec")

    # pylint: disable=unused-variable
    @bp.route("/apispec")
    def apispec():
        return jsonify(generate_api_spec(title=title, version=version, bp_name=bp.name if isinstance(bp, Blueprint) else None, global_params=global_params))

    @bp.route("/api")
    def swagger():
        print("ideyedi")
        return render_template("swagger-ui.html", spec_url=get_api_spec_url())
