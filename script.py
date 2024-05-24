import random

BOARD_ROW_LENGTH = 10
BOARD_COLUMN_LENGTH = 10

MAX_TRIES_TO_PUT_WORD = BOARD_ROW_LENGTH * BOARD_COLUMN_LENGTH

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
    used_words = []
    positions = [] # only for cache
    words = load_words()
    words_with_indexs = build_indexes(words)

    for word in words:
        direction = get_new_direction()
        match try_generate_random_position_to_put(board, direction, word):
          case None:
            board
          case ("another_word", row, column, direction, obstacles_with_positions):
            # find some word that match
            return board
          case (row, column):
            positions.append({word: (row, column)})
            used_words.append(word)
            board = put_on_board(board, row, column, direction, word)

    return (board, positions)

def load_words() -> list:
    accumulator = []
    with open(WORDS_PATH, "r") as reader:
        for word in str(reader.read()).split("\n"):
            if word:
                accumulator.append(word)

    return accumulator

def build_indexes(words: list):
    return list(map(build_letters_with_positions, words))

def build_letters_with_positions(word):
    index = 0
    accumulator = []
    for l in word:
        accumulator.append((l, index))
        index = index + 1
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
    index =  random.randint(0, len(WORD_ALLOWED_DIRECTIONS) - 1)
    return WORD_ALLOWED_DIRECTIONS[index]

def put_on_board(board: list, row: int, column: int, direction: int, word: str) -> list:
    if word == "":
        return board
    else:
        head = word[0]
        tail = word[1:]
        board[row][column] = head
        return put_on_board(
            board,
            next_row_index(row, direction),
            next_column_index(column, direction),
            direction,
            tail
        )

def try_generate_random_position_to_put(board: list, direction: str, word: str, tries: list = []):
    position = generate_new_position()
    
    if position in tries:
        return (
            None if len(tries) == MAX_TRIES_TO_PUT_WORD
            else try_generate_random_position_to_put(board, direction, word, tries + [position])
        )

    direction_is_used = direction_is_been_used(board, position, direction)
    word_fit = is_word_fit(board, position, direction, word)
    
    if not direction_is_used and word_fit:
         match get_obstacles(board, position, direction, word):
           case "no_obstacles":
             return position

           case ("obstacles", obstacles):
             print("obstacles: " + str(obstacles))
             print("word: " + word)
             #return ("obstacles", obstacles)
             return position
    else:
        return (
            None if len(tries) == MAX_TRIES_TO_PUT_WORD
            else try_generate_random_position_to_put(board, direction, word, tries + [position])
        )

def get_obstacles(board, position, direction, word):
    (row, column) = position
    word_len = len(word)
    obstacles = []
    for index in range(0, word_len):
        next_row = next_row_index(row, direction, index)
        next_column = next_column_index(column, direction, index)

        if not next_row_is_exceeded(next_row) and not next_column_is_exceeded(next_column):
            if cell := board[next_row][next_column]:
                obstacles.append({cell: index})

    ## Checar `obstacles`
    if len(obstacles) == 0:
        return "no_obstacles"
    else:
        return ("obstacles", obstacles)

def is_word_fit(board: list, position: tuple, direction: str, word: str) -> bool:
    word_len = len(word)
    (row, column) = position
    last_row_index = next_row_index(row, direction, times=word_len)
    last_column_index = next_column_index(column, direction, times=word_len)
    return not next_row_is_exceeded(last_row_index) and not next_column_is_exceeded(last_column_index)

def direction_is_been_used(board: list, position: tuple, direction: str) -> list:
    (row, column) = position
    next_row = next_row_index(row, direction)
    next_column = next_column_index(column, direction)

    if next_row_is_exceeded(next_row) or next_column_is_exceeded(next_column):
        return False

    return board[next_row][next_column]

def next_row_index(row: str, direction: str, times: int = 1):
    if direction in ["vertical_up", "diagonal_up_left", "diagonal_up_right"]:
        return row - times
    elif direction in ["vertical_down", "diagonal_down_left", "diagonal_down_right"]:
        return row + times
    elif direction in ["horizontal_left", "horizontal_right"]:
        return row
    else:
        raise RuntimeError("wrong direction - got: {}".format(direction))

def next_column_index(column: int, direction: str, times: int = 1):
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
