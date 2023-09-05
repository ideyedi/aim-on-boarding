import json

from flask import request
from flask_apispec import doc, use_kwargs, marshal_with
from flask_classful import FlaskView, route
from flask_api import status

from app.schema.board import *
from core.user import check_access_token
from app.error import ApiErrorSchema, ApiError
from app.service.board import BoardService


class BoardView(FlaskView):

    @doc(tags=["Board"], summary="Board feature health-check")
    @route("monitor", methods=["GET"])
    def healthcheck(self):
        return ("Board healthCheck",
                status.HTTP_200_OK)

    @doc(tags=["Board"], summary="Board feature", description="게시판 생성")
    @route("", methods=["POST"])
    @check_access_token
    @use_kwargs(BoardCreateSchema, location="json_or_form", inherit=True, apply=False)
    @marshal_with(ApiErrorSchema(), code=422, description="정상적이지만 서비스에서 처리 불가능")
    def create_board(self, **kwargs):
        in_board = BoardCreateSchema().load(request.get_json())
        #print(type(request.get_json()), request.get_json())
        if in_board is False:
            raise ApiError("Duplicated Title",
                           status_code=status.HTTP_409_CONFLICT)

        board_service = BoardService(in_board)
        # Board service setter
        board_service.admin = kwargs["user_id"]

        ret = board_service.create_board()
        if ret is not True:
            raise ApiError("Failed to create board",
                           status_code=status.HTTP_406_NOT_ACCEPTABLE)

        return ("Create board",
                status.HTTP_200_OK)

    @doc(tags=["Board"], summary="Board feature", description="게시판 삭제")
    @route("", methods=["DELETE"])
    @check_access_token
    @use_kwargs(BoardDeleteSchema, location="json_or_form", inherit=True, apply=False)
    def delete_board(self, **kwargs):
        in_board = BoardDeleteSchema().load(request.get_json())
        if in_board is False:
            raise ApiError("Create failed",
                           status.HTTP_400_BAD_REQUEST)

        board_service = BoardService(in_board)
        board_service.admin = kwargs["user_id"]
        ret = board_service.delete_board()
        print(f"{__name__} {ret}")
        return ("Delete board",
                status.HTTP_200_OK)

    @doc(tags=["Board"], summary="Board feature", description="게시판 수정")
    @route("", methods=["PATCH"])
    @check_access_token
    @use_kwargs(BoardInfoSchema(), location="query")
    def modify_board(self, model_board, **kwargs):
        board_service = BoardService(model_board)

        if not kwargs["user_id"]:
            # Error handler에서 아에 서비스가 죽어버리면 안됨.. 처리 필요
            return ApiError("Unauthorized User",
                           status_code=status.HTTP_401_UNAUTHORIZED)
        else:   # Debug
            print(kwargs["user_id"])

        board_service.admin = kwargs["user_id"]
        ret = board_service.modify_board()

        if not ret:
            return ("Couldn't modified data",
                    status.HTTP_405_METHOD_NOT_ALLOWED)

        return ("Modify board",
                status.HTTP_200_OK)
