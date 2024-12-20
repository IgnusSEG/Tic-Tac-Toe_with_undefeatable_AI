import sys   
import pygame
import numpy as np

pygame.init()  
#Colors
White = (255, 255, 255)
Gray = (128, 128, 128)
Red = (255, 0, 0)
Black = (0, 0, 0)
Green = (0, 255, 0)

#Board Size
Width = 400
Height = 400
Line_Width = 5
Board_Rows = 3
Board_Columns = 3
Square_Size = Width // Board_Columns
Circle_Radius = Square_Size // 3
Circle_Width = 10
Cross_Width = 20

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('Tic Tac Toe VS. AI')
screen.fill(Black)
board = np.zeros((Board_Rows, Board_Columns))

def draw_lines(color = White):
    for i in range(1, Board_Rows):
        pygame.draw.line(screen, color, (0, Square_Size * i), (Width, Square_Size * i), Line_Width)
        pygame.draw.line(screen, color, (Square_Size * i, 0), (Square_Size * i, Height), Line_Width)


def draw_figures(color = White):
    for row in range(Board_Rows):
        for column in range(Board_Columns):
            if board[row][column] == 1:
                pygame.draw.circle(screen, color, (int(column * Square_Size + Square_Size // 2), int(row * Square_Size + Square_Size // 2)), Circle_Radius, Circle_Width)
            elif board[row][column] == 2:
                pygame.draw.line(screen, color, (column * Square_Size + Square_Size // 4, row * Square_Size + Square_Size // 4), (column * Square_Size + 3 * Square_Size // 4, row * Square_Size + 3 * Square_Size // 4), Cross_Width)
                pygame.draw.line(screen, color, (column * Square_Size + Square_Size // 4, row * Square_Size + 3 * Square_Size // 4), (column * Square_Size + 3 * Square_Size // 4, row * Square_Size + Square_Size // 4), Cross_Width)


def mark_square(row, column, player):
    board[row][column] = player

def available_square(row, column):
    return board[row][column] == 0

def is_board_full(check_board = board):
    for row in range(Board_Rows):
        for column in range(Board_Columns):
            if check_board[row][column] == 0:
                return False
    return True

def check_win(player, check_board = board):
    for column in range(Board_Columns):
        if check_board[0][column] == player and check_board[1][column] == player and check_board[2][column] == player:
            return True

    for row in range(Board_Rows):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True

    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True

    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    return False

def draw_message(message, color, center):
    font = pygame.font.SysFont('calibri', 50)
    text = font.render(message, True, color)
    screen.blit(text, (center[0] - text.get_width() // 2, center[1] - text.get_height() // 2))

#AI
def minimax(Minimax_Board, depth, isMaximizing):
    if check_win(2, Minimax_Board):
        return float('inf')
    elif check_win(1, Minimax_Board):
        return float('-inf')
    elif is_board_full(Minimax_Board):
        return 0

    if isMaximizing:
        best_score = -100
        for row in range(Board_Rows):
            for column in range(Board_Columns):
                if Minimax_Board[row][column] == 0:
                    Minimax_Board[row][column] = 2
                    score = minimax(Minimax_Board, depth + 1, False)
                    Minimax_Board[row][column] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 100
        for row in range(Board_Rows):
            for column in range(Board_Columns):
                if Minimax_Board[row][column] == 0:
                    Minimax_Board[row][column] = 1
                    score = minimax(Minimax_Board, depth + 1, True)
                    Minimax_Board[row][column] = 0
                    best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -100
    move = (-1, -1)
    for row in range(Board_Rows):
        for column in range(Board_Columns):
            if board[row][column] == 0:
                board[row][column] = 2
                score = minimax(board, 0, False)
                board[row][column] = 0
                if score > best_score:
                    best_score = score
                    move = (row, column)
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False

def restart():
    screen.fill(Black)
    draw_lines()
    for row in range(Board_Rows):
        for column in range(Board_Columns):
            board[row][column] = 0



draw_lines()
player = 1
game_over = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x = event.pos[0] // Square_Size
            mouse_y = event.pos[1] // Square_Size
            if available_square(mouse_y, mouse_x):
                mark_square(mouse_y, mouse_x, player)
                if check_win(player):
                    game_over = True
                player = player % 2 + 1

                if not game_over:
                    if best_move():
                        if check_win(2):
                            game_over = True
                        player = player % 2 + 1
                if not game_over:
                    if is_board_full():
                        game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = 1
                game_over = False

    if not game_over:
        draw_figures()
    else:
        if check_win(1):
            draw_figures(Green)
            draw_lines(Green)
            draw_message('Player Wins!', White, (Width // 2, Height // 2))
        elif check_win(2):
            draw_figures(Red)
            draw_lines(Red)
            draw_message('AI Wins!', White, (Width // 2, Height // 2))
        else:
            draw_figures(Gray)
            draw_lines(Gray)
            draw_message('Tie Game!', White, (Width // 2, Height // 2))

    pygame.display.update()
