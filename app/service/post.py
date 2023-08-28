from app.model.post import Post, Author
from app.model.board import Board
from app.model.user import User

from datetime import datetime


class PostService:
    def __init__(self, post: Post):
        self._post_model = post

    def creat_post(self, board_title: str, user_id: str):
        self._post_model.create_time = datetime.now()

        board_model = Board.objects(board_name=board_title).first()
        if board_model is False:
            print("[Debug], 해당되는 게시판 정보를 가지고 오지 못함")
            return False

        user_model = User.objects(user_id=user_id).first()

        self._post_model.board = board_model
        self._post_model.author = Author(user_id=user_model.user_id)

        print(user_id)
        ret = self._post_model.save()
        print(f"{__name__}, {ret}, {self._post_model.board.board_name}")

        return True

