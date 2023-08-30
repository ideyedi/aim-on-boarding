from flask import g, request
from flask_apispec import doc, use_kwargs, marshal_with
from flask_classful import FlaskView, route
from flask_api import status


class CommentView(FlaskView):

    @doc(tags=["Comment"], summary="Comment feature", description="health-check monitor")
    @route("monitor", methods=["GET"])
    def dashboard_monit(self):
        return ("Comment health-check",
                status.HTTP_200_OK)

