from app.model.board import Board


class BoardService:
    def __init__(self, board: Board):
        self.board = board

    @property
    def get_name(self):
        return self.board.board_name

    @property
    def get_description(self):
        return self.board.description

    def create_board(self):
        test = self.get_name
        print(test)
