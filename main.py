from pygame import *
import pygame
from Board import Board
from Piece import Piece
dimensions = [1000, 820]

init()
screen = display.set_mode(dimensions)

screen.fill((0, 0, 0))

top_white_board = Vector2(0, 0)
bot_white_board = Vector2(0, 420)
top_black_board = Vector2(600, 0)
bot_black_board = Vector2(600, 420)
board_dimensions = Vector2(400, 400)
separating_line = Vector2(0, 400)
separating_line_dimensions = Vector2(1000, 20)
board_size = 4
white = Vector3(229, 225, 206)
brown = Vector3(139, 69, 19)
gold = Vector3(205, 130, 41)
black = Vector3(0, 0, 0)
white_piece_color = Vector3(255, 252, 250)
black_piece_color = Vector3(40,40,40)

color_dict = {"white": white_piece_color, "black": black_piece_color, "select": (255, 0, 0), "white_board": white,
              "black_board": brown}

boards = []
prev_data = None
prev_piece = None


def init_board():
    pygame.draw.rect(screen, white, (top_white_board, board_dimensions))
    pygame.draw.rect(screen, white, (bot_white_board, board_dimensions))
    pygame.draw.rect(screen, brown, (top_black_board, board_dimensions))
    pygame.draw.rect(screen, brown, (bot_black_board, board_dimensions))
    for i in range(board_size-1):
        line_pos = (i+1)*(board_dimensions.x/board_size)
        pygame.draw.line(screen, black, (line_pos,0), (line_pos, board_dimensions.x*2+separating_line_dimensions.y), 1)
        pygame.draw.line(screen, black, (line_pos+top_black_board.x, 0), (line_pos+top_black_board.x, board_dimensions.x * 2+separating_line_dimensions.y), 1)
        pygame.draw.line(screen, black, (0, line_pos), (board_dimensions.x*3, line_pos), 1)
        pygame.draw.line(screen, black, (0, line_pos+bot_white_board.y), (board_dimensions.x * 3, line_pos+bot_white_board.y), 1)
    pygame.draw.rect(screen, gold, (separating_line, separating_line_dimensions))


def draw_piece(piece: Piece):
    assert piece, "Trying to draw a non-existent piece"
    board_pos = piece.board_pos
    increment = Vector2(50, 50)
    if board_pos[0] == 1:
        increment += Vector2(top_black_board.x, 0)
    if board_pos[1] == 1:
        increment += Vector2(0, bot_black_board.y)
    middle = Vector2(piece.pos)*100 + increment
    pygame.draw.circle(screen, color_dict[piece.color], middle, 30)


def screen_to_piece(pos):
    pos = list(pos)
    board = [0, 0]
    if pos[0] > 600:
        pos[0] -= 600
        board[0] = 1
    elif 400 < pos[0] < 600:
        return None
    if pos[1] > 420:
        pos[1] -= 420
        board[1] = 1
    elif 400 < pos[1] < 420:
        return None
    # temp = pos[1]
    # pos[1] = pos[0]
    # pos[0] = temp
    return [int(c/100) for c in pos], board


def setup():
    init_board()
    global boards
    boards = [Board(4, (i, j)) for i in range(2) for j in range(2)]
    for b in boards:
        for row in b.board:
            for piece in row:
                if piece:
                    draw_piece(piece)


def draw():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                try:
                    global boards, prev_data, prev_piece
                    piece_data = screen_to_piece(mouse.get_pos())  # Current pos
                    if not piece_data:
                        print("Selected nothing")
                        if prev_piece:
                            draw_piece(prev_piece)
                            prev_data = None
                            prev_piece = None
                        continue
                    piece_pos, board_pos = piece_data
                    current_board = boards[board_pos[1] + board_pos[0] * 2]
                    current_piece = current_board.get_piece(piece_pos)
                    if not prev_data:
                        if not current_piece:
                            print("Selected nothing")
                            continue
                        prev_data = piece_data
                        prev_piece = current_piece
                        draw_piece(Piece(Vector2(piece_pos), "select", Vector2(board_pos)))  # draw the select
                    else:
                        if prev_data == piece_data or board_pos != prev_data[1] or not piece_pos:
                            draw_piece(prev_piece)  # draw the select
                            print("2 bad")
                        else:
                            # TODO MAKE DIFFERENT COLOR
                            if board_pos[0] == 0:
                                empty_space = Piece(Vector2(prev_data[0]), "white_board", Vector2(prev_data[1]))
                            else:
                                empty_space = Piece(Vector2(prev_data[0]), "black_board", Vector2(prev_data[1]))
                            draw_piece(empty_space)
                            current_board.move_piece(prev_data[0], piece_pos)
                            current_piece = current_board.get_piece(piece_pos)
                            draw_piece(current_piece)

                            # print("3d pog", current_board)
                        prev_data = None



                except TypeError as E:
                    raise E
                    print("Cannot draw on black", E)
        display.flip()
    quit()


setup()
draw()
