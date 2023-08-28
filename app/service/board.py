from app.model.board import Board, EmbedUser


class BoardService:
    def __init__(self, board: Board):
        self._board = board
        print(self._board.__repr__())

    @property
    def name(self):
        return self._board.board_name

    @property
    def description(self):
        return self._board.description

    @property
    def admin(self):
        return self._board.admin

    @admin.setter
    def admin(self, admin: str):
        self._board.admin = EmbedUser(user_id=admin)

    def create_board(self):
        print(self._board.__repr__())
        ret = self._board.save()
        return True

    def modify_board(self):
        tmp_model = self._board

        # 해당되는 첫번째 데이터를 수정
        ret = Board.objects(board_name=self._board.board_name,
                            admin=self._board.admin).first()
        if tmp_model.board_name == ret.board_name and tmp_model.admin == ret.admin:
            ret.update(description=self._board.description)
        else:
            return False

        return True

    def delete_board(self):
        # 해당되는 모든 정보를 지우는 방식으로 구현
        ret = Board.objects(board_name=self._board.board_name.name,
                            admin=self._board.admin)
        if ret:
            print(f"Founded \n {ret}")
            ret.delete()
        else:
            print("Not Founded")

        return True
