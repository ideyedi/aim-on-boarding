from flask import request
from flask_apispec import doc, use_kwargs, marshal_with
from flask_classful import FlaskView, route
from flask_api import status

#from app.model.board import Board
from app.schema.board import *
from core.user import check_access_token
from app.error import ApiErrorSchema


class BoardView(FlaskView):

    @doc(summary="Board feature health-check")
    @route("monitor", methods=["GET"])
    def board_monit(self):
        return ("Board healthCheck",
                status.HTTP_200_OK)

    @doc(summary="Board feature, 게시판 생성", description="게시판 생성 endpoint")
    @route("", methods=["POST"])
    @check_access_token
    @use_kwargs(BoardCreateSchema, location="json_or_form")
    @marshal_with(ApiErrorSchema(), code=422, description="??")
    def create_board(self, **kwargs):
        # json body location으로 보내고 싶은데 스웨거 상에서는 조회가 안되는 부분 확인 필요

        return ("Create board",
                status.HTTP_200_OK)
