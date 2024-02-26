class Connect2Board:
    def __init__(self):
        self.board = [0, 0, 0, 0]
        self.history = []
        self.black_turn = False
        self.empty_turn = True

    def submit_move(self, move):
        if not self.empty_turn:
            self.history.append(move)
            if self.black_turn:
                self.board[move] = "B"
            else:
                self.board[move] = "W"
            self.black_turn = not self.black_turn
        self.empty_turn = not self.empty_turn

    def undo_move(self):
        if self.empty_turn:
            self.board[self.history.pop()] = 0
            self.black_turn = not self.black_turn
        self.empty_turn = not self.empty_turn

        # self.board[self.history.pop()] = 0
        # self.black_turn = not self.black_turn

    def get_move_list(self):
        if self.empty_turn:
            return [0, 1]
        return [i for i in range(4) if self.board[i] == 0]

    def is_game_over(self):
        if self.board[0] == self.board[1] or self.board[1] == self.board[2] or self.board[2] == self.board[3]:
            if self.board[1] != 0 and self.board[2] != 0:
                return True
        for i in range(4):
            if self.board[i] == 0:
                return False
        return True

    def get_winner(self):
        if self.board[0] == self.board[1]:
            if (self.black_turn and self.board[0] == "B") or (not self.black_turn and self.board[0] == "W"):
                return 1
            else:
                return -1
        if self.board[1] == self.board[2]:
            if (self.black_turn and self.board[1] == "B") or (not self.black_turn and self.board[1] == "W"):
                return 1
            else:
                return -1
        if self.board[2] == self.board[3]:
            if (self.black_turn and self.board[2] == "B") or (not self.black_turn and self.board[2] == "W"):
                return 1
            else:
                return -1
        return 0

    def __str__(self):
        return str(self.board)
