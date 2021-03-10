from pygame import Vector2
from Piece import Piece


class Board:
    def __init__(self, size, pos):
        self.pos = pos
        self.size = size
        self.board = [[Piece(Vector2(i, j), "white", self.pos) if j == 0 else Piece(Vector2(i, j), "black", self.pos) if j == size-1 else None for j in range(size)] for i in range(size)]

    def __repr__(self):
        rtn = ""
        for j in range(self.size):
            for i in range(self.size):
                if self.board[i][j]:
                    rtn += self.board[i][j].color + " (" + str(i) + ", " + str(j) + ")" + str(self.board[i][j].get_pos())
                else:
                    rtn += "None" + " (" + str(i) + ", " + str(j) + ")"
            rtn += "\r\n"
        return rtn

    def move_piece(self, prev_pos, curr_pos):
        prev_pos = [int(a) for a in prev_pos]
        prev_piece = self.board[prev_pos[0]][prev_pos[1]]
        if not self.is_move_valid(prev_pos, curr_pos):
            return
        prev_piece.place_at(Vector2(curr_pos))
        self.board[prev_pos[0]][prev_pos[1]] = self.board[curr_pos[0]][curr_pos[1]]
        self.board[curr_pos[0]][curr_pos[1]] = prev_piece

    def is_move_valid(self, prev_pos, curr_pos):
        return True

    def get_piece(self, piece_pos):
        return self.board[int(piece_pos[0])][int(piece_pos[1])]
