"""
Algoritmo responsável por localizar uma `position` para as palavras passadas para a função `new_game(loaded_words)`.
Breve glossário do algortimo:
- `position` - dicionário contendo as chaves: 'row', 'column' e 'direction'
- `fit` - termo que significa: palavra caber em determinada `position` (caber significa ter o comprimento igual ou menor e a direção não estar sendo usada)
- `obstacle` - letra que aparece no meio de um `spawn`
- `spawn` - tentativa de colocar uma palavra no `board`
"""

import random
from enum import Enum

BOARD_ROW_LENGTH = 20
BOARD_COLUMN_LENGTH = 20

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

Tags = Enum('Tags', [
    'NO_OBSTACLES',
    'OBSTACLES',
    'WORD_DOESNT_FIT',
    'MATCH_WORD',
    'NO_MATCH_WORD',
    'OK',
    'SUBSTITUTE_WORD'
])

def new_game(loaded_words: list):
    board = build_board()
    positions = [] ## only for future cache
    words = loaded_words.copy()
    helpers = loaded_words.copy()
    
    for word in words:
        helpers_filtered = [w for w in helpers if w != word]
        
        match recursivelly_try_put_word(board, word, positions, helpers_filtered, []):
          case (Tags.OK, word, position):
            positions.append({word: position})
            helpers.remove(word) if word in helpers else None
            board = put_on_board(board, position, word)

          case (Tags.SUBSTITUTE_WORD, substitute_word, position):
            """
            Aqui acontece uma troca, a palavra escolhida como "substituta" ou "match" vai ser removida das palavras "helpers" pois já foi usada
            e será removida do resto das "words" para não ser utilizada novamente. E a palavra que não pode ser encaixada será colocada
            no final da lista das "words" para tentar ser usada em outro momento.
            """
            positions.append({substitute_word: position})
            helpers.remove(substitute_word)
            words.append(word)
            words.remove(substitute_word) if substitute_word in words else None
            board = put_on_board(board, position, substitute_word)

    return (board, positions)

def recursivelly_try_put_word(board: list, word: str, positions: list, helpers: list, tried_positions: str):
    if len(tried_positions) == MAX_TRIES_TO_PUT_WORD:
        return None
    
    match try_generate_random_position_to_put(board, word):
      case (Tags.WORD_DOESNT_FIT, tried_position):
        return recursivelly_try_put_word(board, word, positions, helpers, tried_positions + [tried_position])

      case (Tags.NO_OBSTACLES, position):
        return (Tags.OK, word, position)

      case (Tags.OBSTACLES, obstacles, tried_position, word):
        match handle_obstacles(board, obstacles, positions, tried_position, word, helpers):
          case Tags.NO_MATCH_WORD:
            return recursivelly_try_put_word(
                board,
                word,
                positions,
                helpers,
                tried_positions + [tried_position]
            )

          case (Tags.MATCH_WORD, match_word, position):
            return (Tags.SUBSTITUTE_WORD, match_word, position)


def handle_obstacles(board: list, obstacles: list, positions: list, position: dict, word: str, helpers: list):
    match find_match_word(board, obstacles, position, helpers):
      case (Tags.MATCH_WORD, match_word, position):
        return (Tags.MATCH_WORD, match_word, position)

      case Tags.NO_MATCH_WORD:
        return Tags.NO_MATCH_WORD


def find_match_word(board: list, obstacles: list, position: dict, helper_words: list):
    if len(helper_words) == 0:
        return Tags.NO_MATCH_WORD

    head = helper_words[0]
    counter = 0
    for (obstacle, index) in obstacles:
        word_fit = is_word_fit(board, position, head)
        if (len(head) - 1) >= index and word_fit and head[index] == obstacle:
            counter = counter + 1


    if counter == len(obstacles):
        return (Tags.MATCH_WORD, head, position)
    else:
        return find_match_word(board, obstacles, position, helper_words[1:])

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

def put_on_board(board: list, position: dict, word: str) -> list:
    if word == "":
        return board
    else:
        head = word[0]
        tail = word[1:]

        update_board(board, position, head)

        new_position = update_column(
            update_row(position, next_row_index(position)),
            next_column_index(position)
        )

        return put_on_board(
            board,
            new_position,
            tail
        )

def try_generate_random_position_to_put(board: list, word: str):
    position = new_position()

    direction_is_used = direction_is_been_used(board, position)
    word_fit = is_word_fit(board, position, word)

    if not direction_is_used and word_fit:
         match get_obstacles(board, position, word):
           case Tags.NO_OBSTACLES:
             return (Tags.NO_OBSTACLES, position)

           case (Tags.OBSTACLES, obstacles):
             return (Tags.OBSTACLES, obstacles, position, word)
    else:
        return (Tags.WORD_DOESNT_FIT, position)

def get_obstacles(board, position, word):
    word_len = len(word)
    obstacles = []
    for index in range(0, word_len):
        next_row = next_row_index(position, times=index)
        next_column = next_column_index(position, times=index)
        if not next_row_is_exceeded(position) and not next_column_is_exceeded(position):
            if cell := board[next_row][next_column]:
                obstacles.append((cell, index))

    if len(obstacles) == 0:
        return Tags.NO_OBSTACLES
    else:
        return (Tags.OBSTACLES, obstacles)

def is_word_fit(board: list, position: dict, word: str) -> bool:
    word_len = len(word)
    last_row_index = next_row_index(position, times=word_len)
    last_column_index = next_column_index(position, times=word_len)
    return not next_row_is_exceeded(last_row_index) and not next_column_is_exceeded(last_column_index)

def direction_is_been_used(board: list, position: tuple) -> list:
    next_row = next_row_index(position)
    next_column = next_column_index(position)

    if next_row_is_exceeded(next_row) or next_column_is_exceeded(next_column):
        return False

    return board[next_row][next_column]

def next_row_index(position: dict, times: int = 1):
    row = position["row"]
    direction = position["direction"]

    if direction in ["vertical_up", "diagonal_up_left", "diagonal_up_right"]:
        return row - times
    elif direction in ["vertical_down", "diagonal_down_left", "diagonal_down_right"]:
        return row + times
    elif direction in ["horizontal_left", "horizontal_right"]:
        return row
    else:
        raise RuntimeError("wrong direction - got: {}".format(direction))

def next_column_index(position: dict, times: int = 1):
    column = position["column"]
    direction = position["direction"]

    if direction in ["vertical_up", "vertical_down"]:
        return column
    elif direction in ["horizontal_left", "diagonal_up_left", "diagonal_down_left"]:
        return column - times
    elif direction in ["horizontal_right", "diagonal_up_right", "diagonal_down_right"]:
        return column + times
    else:
        raise RuntimeError("wrong direction - got: " + str(direction))

def next_row_is_exceeded(v):
    if type(v) is int:
        return v >= BOARD_ROW_LENGTH or v < 0
    elif type(v) is dict:
        return v["row"] >= BOARD_ROW_LENGTH or v["row"] < 0
    else:
        raise RuntimeError("wrong argument type - got: " + str(v))

def next_column_is_exceeded(v):
    if type(v) is int:
        return v >= BOARD_COLUMN_LENGTH or v < 0
    else:
        return v["column"] >= BOARD_COLUMN_LENGTH or v["column"] < 0

def on_the_board(board, position):
    return board[position["row"]][position["column"]]

def update_board(board, position, value):
    board[position["row"]][position["column"]] = value

## position object handle
def new_position():
    row = random.randint(0, BOARD_ROW_LENGTH - 1)
    column = random.randint(0, BOARD_COLUMN_LENGTH - 1)
    direction_index = random.randint(0, len(WORD_ALLOWED_DIRECTIONS) - 1)
    
    return {
        "row": row,
        "column": column,
        "direction": WORD_ALLOWED_DIRECTIONS[direction_index],
    }

def update_row(position, new_row):
    position["row"] = new_row
    return position

def update_column(position, new_column):
    position["column"] = new_column
    return position
