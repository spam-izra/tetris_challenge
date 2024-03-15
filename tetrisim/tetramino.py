from enum import Enum

class Tetramino(Enum):
    O = 0
    I = 1
    T = 2
    L = 3
    J = 4
    S = 5
    Z = 6

class Orientation(Enum):
    N = 0
    E = 1
    S = 2
    W = 3

# Сдвиг спрайта относительно позиции центра-2 и верхней части стакана
# Для 10 на 20 - это будет (20, 3)
# (y, x)
START_POSITION = {
    Tetramino.O: (-1, 1),
    Tetramino.I: (-2, 0),
    Tetramino.T: (-1, 0),
    Tetramino.L: (-1, 0),
    Tetramino.J: (-1, 0),
    Tetramino.S: (-1, 0),
    Tetramino.Z: (-1, 0),
}

# У нас внутри координаты стакана идут сверху вниз, а не как на экране снизу вверх.
# Поэтому порядок следования строк обратный

Sprites = {
    Tetramino.O: {
        Orientation.N: [
            [0, 1, 1,],
            [0, 1, 1,],
            [0, 0, 0,],
        ],
        Orientation.E: [
            [0, 1, 1,],
            [0, 1, 1,],
            [0, 0, 0,],
        ],
        Orientation.S: [
            [0, 1, 1,],
            [0, 1, 1,],
            [0, 0, 0,],
        ],
        Orientation.W: [
            [0, 1, 1,],
            [0, 1, 1,],
            [0, 0, 0,],
        ],
    },

    Tetramino.I: {
        Orientation.N: list(reversed([
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])),
        Orientation.E: list(reversed([
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
        ])),
        Orientation.S: list(reversed([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
        ])),
        Orientation.W: list(reversed([
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
        ])),
    },

    Tetramino.T: {
        Orientation.N: list(reversed([
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0],
        ])),
        Orientation.E: list(reversed([
            [0, 1, 0],
            [0, 1, 1],
            [0, 1, 0],
        ])),
        Orientation.S: list(reversed([
            [0, 0, 0],
            [1, 1, 1],
            [0, 1, 0],
        ])),
        Orientation.W: list(reversed([
            [0, 1, 0],
            [1, 1, 0],
            [0, 1, 0],
        ])),
    },

    Tetramino.L: {
        Orientation.N: list(reversed([
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0],
        ])),
        Orientation.E: list(reversed([
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 1],
        ])),
        Orientation.S: list(reversed([
            [0, 0, 0],
            [1, 1, 1],
            [1, 0, 0],
        ])),
        Orientation.W: list(reversed([
            [1, 1, 0],
            [0, 1, 0],
            [0, 1, 0],
        ])),
    },

    Tetramino.J: {
        Orientation.N: list(reversed([
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0],
        ])),
        Orientation.E: list(reversed([
            [0, 1, 1],
            [0, 1, 0],
            [0, 1, 0],
        ])),
        Orientation.S: list(reversed([
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 1],
        ])),
        Orientation.W: list(reversed([
            [0, 1, 0],
            [0, 1, 0],
            [1, 1, 0],
        ])),
    },

    Tetramino.S: {
        Orientation.N: list(reversed([
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0],
        ])),
        Orientation.E: list(reversed([
            [0, 1, 0],
            [0, 1, 1],
            [0, 0, 1],
        ])),
        Orientation.S: list(reversed([
            [0, 0, 0],
            [0, 1, 1],
            [1, 1, 0],
        ])),
        Orientation.W: list(reversed([
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 0],
        ])),
    },

    Tetramino.Z: {
        Orientation.N: list(reversed([
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0],
        ])),
        Orientation.E: list(reversed([
            [0, 0, 1],
            [0, 1, 1],
            [0, 1, 0],
        ])),
        Orientation.S: list(reversed([
            [0, 0, 0],
            [1, 1, 0],
            [0, 1, 1],
        ])),
        Orientation.W: list(reversed([
            [0, 1, 0],
            [1, 1, 0],
            [1, 0, 0],
        ])),
    },
}