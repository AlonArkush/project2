from pygame import Vector2


class Piece:
    def __init__(self, pos: Vector2, color, board_pos: Vector2):
        self.pos = Vector2(pos)
        self.color = color
        self.board_pos = board_pos

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_pos(self):
        return self.pos

    def move(self, direction: Vector2):
        self.pos += direction

    def place_at(self, pos: Vector2):
        self.pos = pos
