import random

BOARD_ROW_LENGTH = 7
BOARD_COLUMN_LENGTH = 7

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
    positions = [] # only for cache
    used_words = []
    words = load_words()

    for word in words:
        match try_generate_random_position_to_put(board,  word):
          case ("obstacles", obstacles, position, word, direction):
            match find_match_word(board, obstacles, direction, position, words, used_words):
              case ("word", match_word):
                (row, column) = position
                positions.append({word: position})
                used_words.append(match_word)
                board = put_on_board(board, row, column, direction, word)

          case (row, column, direction):
            positions.append({word: (row, column)})
            used_words.append(word)
            board = put_on_board(board, row, column, direction, word)

    return (board, positions)

def find_match_word(board: list, obstacles: list, direction: str, position: tuple, words: list, used_words: list):
    if len(words) == 0:
        return None

    head = words[0]    
    counter = 0
    for (obstacle, index) in obstacles:
        word_fit = is_word_fit(board, position, direction, head)
        if (len(head) - 1) >= index and word_fit and head[index] and head not in used_words:
            counter = counter + 1


    if counter == len(obstacles):
        ## TODO: fix
        #return ("match_word", head)
        return None
    else:
        return find_match_word(board, obstacles, direction, position, words[1:], used_words)

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

def try_generate_random_position_to_put(board: list, word: str, tries: list = []):
    position = generate_new_position()
    direction = get_new_direction()
    
    ## cache
    if merge_position_with_direction(position, direction) in tries:
        return (
            None if len(tries) == MAX_TRIES_TO_PUT_WORD
            else try_generate_random_position_to_put(
                    board,
                    word,
                    tries
            )
        )

    direction_is_used = direction_is_been_used(board, position, direction)
    print("CURRENT DIRECTION: " + direction)
    word_fit = is_word_fit(board, position, direction, word)
    
    if not direction_is_used and word_fit:
         match get_obstacles(board, position, direction, word):
           case "no_obstacles":
             (row, column) = position
             return (row, column, direction)

           case ("obstacles", obstacles):
             return ("obstacles", obstacles, position, word, direction)
    else:
        return (
            None if len(tries) == MAX_TRIES_TO_PUT_WORD
            else try_generate_random_position_to_put(
                    board,
                    word,
                    tries + [merge_position_with_direction(position, direction)]
            )
        )

def merge_position_with_direction(position, direction):
    (row, column) = position
    return (row, column, direction)    

def get_obstacles(board, position, direction, word):
    (row, column) = position
    word_len = len(word)
    obstacles = []
    for index in range(0, word_len):
        next_row = next_row_index(row, direction, index)
        next_column = next_column_index(column, direction, index)

        if not next_row_is_exceeded(next_row) and not next_column_is_exceeded(next_column):
            if cell := board[next_row][next_column]:
                obstacles.append((cell, index))

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
