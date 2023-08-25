from app.model.board import Board, EmbedUser


class BoardService:
    def __init__(self, board: Board):
        self._board = board

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
        pass

    def delete_board(self):
        print(self._board.board_name)
        # 해당되는 모든 정보를 지우는 방식으로 구현
        ret = Board.objects(board_name=self._board.board_name,
                            admin=self._board.admin)
        print(type(ret))
        if ret:
            print(f"Founded \n {ret}")
            ret.delete()
        else:
            print("Not Founded")

        return True
