from app.model.post import Post, Author
from app.model.board import Board
from app.model.user import User

from datetime import datetime
from typing import List


class PostService:
    def __init__(self, post: Post):
        self._post_model = post

    def creat_post(self, board_title: str, user_id: str) -> bool:
        board_model = Board.objects(board_name=board_title).first()
        if board_model is False:
            print("[Debug], 해당되는 게시판 정보를 가지고 오지 못함")
            return False

        user_model = User.objects(user_id=user_id).first()

        self._post_model.board = board_model
        self._post_model.author = Author(user_id=user_model.user_id)
        self._post_model.like = []
        ret = self._post_model.save()
        print(f"{__name__}, {ret}, {self._post_model.board.board_name}")

        return True

    def add_like(self, post_id, user_id) -> bool:
        self._post_model = Post.objects(id=post_id).first()

        #
        like_user = User.objects.get(user_id=user_id)
        self._post_model.like.append(like_user)

        ret = self._post_model.save()
        if not ret:
            return False

        return True

    def delete_post(self, post_id, user_id) -> bool:
        self._post_model = Post.objects(id=post_id).first()
        if self._post_model is None:
            return False

        if self._post_model.author.user_id != user_id:
            print("해당 포스트의 작성자가 아닙니다.")
            return False

        ret = self._post_model.delete()
        if not ret:
            print("in if?")
            return False

        return True

    def modify_post(self, post_id, user_id) -> bool:
        tmp_model = Post.objects(id=post_id).first()
        if tmp_model is None:
            return False

        if tmp_model.author.user_id != user_id:
            print("해당 포스트의 작성자가 아닙니다.")
            return False
        # 중복되는 예외처리는 최소화하는 게 좋지
        ret = tmp_model.update(title=self._post_model.title,
                               hashtag=self._post_model.hashtag,
                               modified_time=datetime.now().utcnow())
        if not ret:
            return False

        return True
