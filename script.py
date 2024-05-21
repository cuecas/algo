import random

BOARD_ROW_LENGTH = 10
BOARD_COLUMN_LENGTH = 10

WORD_ALLOWED_DIRECTIONS = [
    "vertical_up",
    "vertical_down",
    "horizontal_left",
    "horizontal_right",
    "diagonal_up_left",
    "diagonal_up_right",
    "diagonal_down_left",
    "diagonal_down_right"
]

def new_game(words: list):
    return None

def build_board() -> list:
    board = []
    for i in range(0, BOARD_ROW_LENGTH):
        colum = []
        for j in range(0, BOARD_COLUMN_LENGTH):
            colum.append(None)
        board.append(colum)
            
    return board

def visualize_board(board: list) -> None:
    for i in board:
        print(i)

def get_new_position() -> tuple:
    row = random.randint(0, BOARD_ROW_LENGTH - 1)
    column = random.randint(0, BOARD_COLUMN_LENGTH - 1)
    return (row, column)

def get_new_direction() -> int:
    indice =  random.randint(0, len(WORD_ALLOWED_DIRECTIONS) - 1)
    return WORD_ALLOWED_DIRECTIONS[indice]

def put_on_board(board: list, row: int, column: int, direction: int, word: str) -> list:
    if word == "":
        return board
    else:
        head = word[0]
        tail = word[1:]
        board[row][column] = head
        return put_on_board(
            board,
            next_row_indice(row, direction),
            next_column_indice(column, direction),
            direction,
            tail
        )

def generate_random_position_to_put(board: list, direction: str, word: str) -> tuple:
    (row, column) = get_new_position()

    if board[row][column]:
        if direction_is_been_used(board, row, column, direction):
            return generate_random_position_to_put(board, direction, word)
        else:
            return (row, column)
    elif is_word_fit(board, row, column, direction, word):
        return (row, column)
    else:
        return generate_random_position_to_put(board, direction, word)

def is_word_fit(board: list, row: int, column: int, direction: str, word: str) -> bool:
    word_len = len(word) - 1
    last_row_index = next_row_indice(row, direction, times=word_len)
    last_column_index = next_column_indice(column, direction, times=word_len)

    if direction in ["vertical_up"]:
        return last_row_index > 0
    elif direction in ["vertical_down"]:
        return last_row_index < BOARD_ROW_LENGTH
    elif direction in ["horizontal_right"]:
        return last_column_index < BOARD_COLUMN_LENGTH
    elif direction in ["horizontal_left"]:
        return last_column_index >= 0
    elif direction in ["diagonal_up_left"]:
        return last_row_index >= 0 and last_column_index > 0
    elif direction in ["diagonal_up_right"]:
        return last_row_index >= 0 and last_column_index < BOARD_COLUMN_LENGTH
    elif direction in ["diagonal_down_left"]:
        return last_row_index < BOARD_ROW_LENGTH and last_column_index > 0
    elif direction in ["diagonal_down_right"]:
        return last_row_index < BOARD_ROW_LENGTH and last_column_index < BOARD_COLUMN_LENGTH

def direction_is_been_used(board: list, row: int, column: int, direction: str) -> list:
    return board[next_row_indice(direction, row)][next_column_indice(direction, column)]

def put_on_direction(word: str, board: list, start_row: int, start_column: int, direction: str):
    for l in word:
        return None

def next_row_indice(row: str, direction: str, times=1):
    if direction in ["vertical_up", "diagonal_up_left", "diagonal_up_right"]:
        return row - times
    elif direction in ["vertical_down", "diagonal_down_left", "diagonal_down_right"]:
        return row + times
    elif direction in ["horizontal_left", "horizontal_right"]:
        return row
    else:
        raise RuntimeError("wrong direction - got: " + direction)

def next_column_indice(column: int, direction: str, times=1):
    if direction in ["vertical_up", "vertical_down"]:
        return column
    elif direction in ["horizontal_left", "diagonal_up_left", "diagonal_down_left"]:
        return column - times
    elif direction in ["horizontal_right", "diagonal_up_right", "diagonal_down_right"]:
        return column + times
    else:
        raise RuntimeError("wrong direction - got: " + direction)

## Tests
board = build_board()
direction = get_new_direction()
word = "carlao"
(row, column) = generate_random_position_to_put(board, direction, word)
board = put_on_board(board, row, column, direction, word)
visualize_board(board)
