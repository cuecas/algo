"""
Modulo responsável por iniciar um jogo novo baseado em um tema.
Cada tema possui determinado número de palavras e parte delas são destinadas
para serem "helpers", ou seja, palavras que facilmente se encaixam caso as palavras "principais"
não consigam ser encaixadas.

O "board" do caça palavras tem o tamanho de 20x20 e deve ter 15 palavras "principais" e no mínimo 5 "helpers"
"""

from algo import new_game
import random

WORDS_FOLDER = "words/"
PRINCIPAL_WORDS_LIMIT = 15 # 15

def animals():
    return new_game(__load_words("animals.txt"))

def __load_words(file: str) -> list:
    accumulator = []
    with open(WORDS_FOLDER + file, "r") as reader:
        for word in str(reader.read()).split("\n"):
            if word:
                accumulator.append(word)

    random.shuffle(accumulator)
    principal = accumulator[0:PRINCIPAL_WORDS_LIMIT]
    helpers = [w for w in accumulator if w not in principal]

    return (principal, helpers)

