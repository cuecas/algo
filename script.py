import random

BOARD_ROW_LENGTH = 10
BOARD_COLUMN_LENGTH = 10

MAX_TRIES_TO_PUT_WORD = 20

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

WORDS_PATH = "words.txt"

def new_game():
    board = build_board()

    for word in load_words():
        direction = get_new_direction()
        match generate_random_position_to_put(board, direction, word):
          case None:
            board
          case (row, column):
            board = put_on_board(board, row, column, direction, word)

    return board

def load_words() -> list:
    accumulator = []
    with open(WORDS_PATH, "r") as reader:
        for word in str(reader.read()).split("\n"):
            if word:
                accumulator.append(word)

    return accumulator

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

def generate_new_position() -> tuple:
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

def generate_random_position_to_put(board: list, direction: str, word: str, tries: int = 1):
    (row, column) = generate_new_position()
    
    direction_is_used = direction_is_been_used(board, row, column, direction)
    word_fit = is_word_fit(board, row, column, direction, word)
    
    if not direction_is_used and word_fit:
        if there_is_any_words_on_the_way(board, row, column, direction, word):
            # TODO: algoritmo de cruzamento
            return (row, column)
        else:
            return (row, column)
    else:
        return (
            None if tries == MAX_TRIES_TO_PUT_WORD
            else generate_random_position_to_put(board, direction, word, tries + 1)
        )

def there_is_any_words_on_the_way(board, row, column, direction, word):
    word_len = len(word) - 1

    for number in range(0, word_len):
        next_row = next_row_indice(row, direction, number)
        next_column = next_column_indice(column, direction, number)

        if next_row_is_exceeded(next_row) or next_column_is_exceeded(next_column):
           return False 
        elif board[next_row][next_column]:
            return True

def is_word_fit(board: list, row: int, column: int, direction: str, word: str) -> bool:
    word_len = len(word)
    last_row_index = next_row_indice(row, direction, times=word_len)
    last_column_index = next_column_indice(column, direction, times=word_len)
    return not next_row_is_exceeded(last_row_index) and not next_column_is_exceeded(last_column_index)

def direction_is_been_used(board: list, row: int, column: int, direction: str) -> list:
    next_row = next_row_indice(row, direction)
    next_column = next_column_indice(column, direction)

    if next_row_is_exceeded(next_row) or next_column_is_exceeded(next_column):
        return False

    return board[next_row][next_column]

def next_row_indice(row: str, direction: str, times: int = 1):
    if direction in ["vertical_up", "diagonal_up_left", "diagonal_up_right"]:
        return row - times
    elif direction in ["vertical_down", "diagonal_down_left", "diagonal_down_right"]:
        return row + times
    elif direction in ["horizontal_left", "horizontal_right"]:
        return row
    else:
        raise RuntimeError("wrong direction - got: {}".format(direction))

def next_column_indice(column: int, direction: str, times: int = 1):
    if direction in ["vertical_up", "vertical_down"]:
        return column
    elif direction in ["horizontal_left", "diagonal_up_left", "diagonal_down_left"]:
        return column - times
    elif direction in ["horizontal_right", "diagonal_up_right", "diagonal_down_right"]:
        return column + times
    else:
        raise RuntimeError("wrong direction - got: " + str(direction))

def next_row_is_exceeded(row):
    return row >= BOARD_ROW_LENGTH or row < 0

def next_column_is_exceeded(column):
    return column >= BOARD_COLUMN_LENGTH or column < 0

board = new_game()
visualize_board(board)
