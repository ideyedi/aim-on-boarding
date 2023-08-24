from flask import request
from flask_apispec import doc
from flask_classful import FlaskView, route
from flask_api import status


class BoardView(FlaskView):

    @doc(summary="Board feature health-check")
    @route("monitor", methods=["GET"])
    def board_monit(self):
        return ("Board healthCheck",
                status.HTTP_200_OK)

    @doc(summary="Board feature, 게시판 생성", description="게시판 생성 endpoint")
    @route("", methods=["POST"])
    def create_board(self):

        return ("Create board",
                status.HTTP_200_OK)
