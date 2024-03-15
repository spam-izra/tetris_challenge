
from .tetramino import Tetramino, Orientation
from .commands import Command

TBLOCK = {
    Orientation.N: {
        Command.COUNTERCLOCKWISE: (Orientation.W, [
            ( 0,  0),
            ( 0, +1),
            (+1, +1),
            (-2, +1),
        ]),
        Command.CLOCKWISE: (Orientation.E, [
            ( 0,  0),
            ( 0, -1),
            (+1, -1),
            (-2, -1),
        ]),
    },

    Orientation.E: {
        Command.COUNTERCLOCKWISE: (Orientation.N, [
            ( 0,  0),
            ( 0, +1),
            (-1, +1),
            (+2,  0),
            (+2, +1),
        ]),
        Command.CLOCKWISE: (Orientation.S, [
            ( 0,  0),
            ( 0, +1),
            (-1, +1),
            (+2,  0),
            (+2, +1),
        ]),
    },

    Orientation.S: {
        Command.COUNTERCLOCKWISE: (Orientation.E, [
            ( 0,  0),
            ( 0, -1),
            (-2,  0),
            (-2, -1),
        ]),
        Command.CLOCKWISE: (Orientation.W, [
            ( 0,  0),
            ( 0, +1),
            (-2,  0),
            (-2, +1),
        ]),
    },

    Orientation.W: {
        Command.COUNTERCLOCKWISE: (Orientation.S, [
            ( 0,  0),
            ( 0, -1),
            (-1, -1),
            (+2,  0),
            (+2, -1),
        ]),
        Command.CLOCKWISE: (Orientation.N, [
            ( 0,  0),
            ( 0, -1),
            (-1, -1),
            (+2,  0),
            (+2, -1),
        ]),
    },
}

OBLOCK = {
    Orientation.N: {
        Command.COUNTERCLOCKWISE: (Orientation.W, [
            (0, 0),
        ]),
        Command.CLOCKWISE: (Orientation.E, [
            (0, 0),
        ]),
    },

    Orientation.E: {
        Command.COUNTERCLOCKWISE: (Orientation.N, [
            (0, 0),
        ]),
        Command.CLOCKWISE: (Orientation.S, [
            (0, 0),
        ]),
    },

    Orientation.S: {
        Command.COUNTERCLOCKWISE: (Orientation.E, [
            (0, 0),
        ]),
        Command.CLOCKWISE: (Orientation.W, [
            (0, 0),
        ]),
    },

    Orientation.W: {
        Command.COUNTERCLOCKWISE: (Orientation.S, [
            (0, 0),
        ]),
        Command.CLOCKWISE: (Orientation.N, [
            (0, 0),
        ]),
    },
}

IBLOCK = {
    Orientation.N: {
        Command.COUNTERCLOCKWISE: (Orientation.W, [
            ( 0,  0),
            ( 0, -1),
            ( 0, +2),
            (+2, -1),
            (-1, +2),
        ]),
        Command.CLOCKWISE: (Orientation.E, [
            ( 0,  0),
            ( 0, -2),
            ( 0, +1),
            (-1, -2),
            (+2, +1),
        ]),
    },

    Orientation.E: {
        Command.COUNTERCLOCKWISE: (Orientation.N, [
            ( 0,  0),
            ( 0, +2),
            ( 0, -1),
            (+1, +2),
            (-2, -1),
        ]),
        Command.CLOCKWISE: (Orientation.S, [
            ( 0,  0),
            ( 0, -1),
            ( 0, +2),
            (+2, -1),
            (-1, +2),
        ]),
    },

    Orientation.S: {
        Command.COUNTERCLOCKWISE: (Orientation.E, [
            ( 0,  0),
            ( 0, +1),
            ( 0, -2),
            (-2, +1),
            (+1, -2),
        ]),
        Command.CLOCKWISE: (Orientation.W, [
            ( 0,  0),
            ( 0, +2),
            ( 0, -1),
            (+1, +2),
            (-2, -1),
        ]),
    },

    Orientation.W: {
        Command.COUNTERCLOCKWISE: (Orientation.S, [
            ( 0,  0),
            ( 0, -2),
            ( 0, +1),
            (-1, -2),
            (+2, +1),
        ]),
        Command.CLOCKWISE: (Orientation.N, [
            ( 0,  0),
            ( 0, +1),
            ( 0, -2),
            (-2, +1),
            (+1, -2),
        ]),
    },
}

LBLOCK = {
    Orientation.N: {
        Command.COUNTERCLOCKWISE: (Orientation.W, [
            ( 0,  0),
            ( 0, +1),
            (+1, +1),
            (-2,  0),
            (-2, +1),
        ]),
        Command.CLOCKWISE: (Orientation.E, [
            ( 0,  0),
            ( 0, -1),
            (+1, -1),
            (-2,  0),
            (-2, -1),
        ]),
    },

    Orientation.E: {
        Command.COUNTERCLOCKWISE: (Orientation.N, [
            ( 0,  0),
            ( 0, +1),
            (-1, +1),
            (+2,  0),
            (+2, +1),
        ]),
        Command.CLOCKWISE: (Orientation.S, [
            ( 0,  0),
            ( 0, +1),
            (-1, +1),
            (+2,  0),
            (+2, +1),
        ]),
    },

    Orientation.S: {
        Command.COUNTERCLOCKWISE: (Orientation.E, [
            ( 0,  0),
            ( 0, -1),
            (+1, -1),
            (-2,  0),
            (-2, -1),
        ]),
        Command.CLOCKWISE: (Orientation.W, [
            ( 0,  0),
            ( 0, +1),
            (+1, +1),
            (-2,  0),
            (-2, +1),
        ]),
    },

    Orientation.W: {
        Command.COUNTERCLOCKWISE: (Orientation.S, [
            ( 0,  0),
            ( 0, -1),
            (-1, -1),
            (+2,  0),
            (+2, -1),
        ]),
        Command.CLOCKWISE: (Orientation.N, [
            ( 0,  0),
            ( 0, -1),
            (-1, -1),
            (+2,  0),
            (+2, -1),
        ]),
    },
}

JBLOCK = {
    Orientation.N: {
        Command.COUNTERCLOCKWISE: (Orientation.W, [
            ( 0,  0),
            ( 0, +1),
            (+1, +1),
            (-2,  0),
            (-2, +1),
        ]),
        Command.CLOCKWISE: (Orientation.E, [
            ( 0,  0),
            ( 0, -1),
            (+1, -1),
            (-2,  0),
            (-2, -1),
        ]),
    },

    Orientation.E: {
        Command.COUNTERCLOCKWISE: (Orientation.N, [
            ( 0,  0),
            ( 0, +1),
            (-1, +1),
            (+2,  0),
            (+2, +1),
        ]),
        Command.CLOCKWISE: (Orientation.S, [
            ( 0,  0),
            ( 0, +1),
            (-1, +1),
            (+2,  0),
            (+2, +1),
        ]),
    },

    Orientation.S: {
        Command.COUNTERCLOCKWISE: (Orientation.E, [
            ( 0,  0),
            ( 0, -1),
            (+1, -1),
            (-2,  0),
            (-2, -1),
        ]),
        Command.CLOCKWISE: (Orientation.W, [
            ( 0,  0),
            ( 0, +1),
            (+1, +1),
            (-2,  0),
            (-2, +1),
        ]),
    },

    Orientation.W: {
        Command.COUNTERCLOCKWISE: (Orientation.S, [
            ( 0,  0),
            ( 0, -1),
            (-1, -1),
            (+2,  0),
            (+2, -1),
        ]),
        Command.CLOCKWISE: (Orientation.N, [
            ( 0,  0),
            ( 0, -1),
            (-1, -1),
            (+2,  0),
            (+2, -1),
        ]),
    },
}

SBLOCK = {
    Orientation.N: {
        Command.COUNTERCLOCKWISE: (Orientation.W, [
            ( 0,  0),
            ( 0, +1),
            (+1, +1),
            (-2,  0),
            (-2, +1),
        ]),
        Command.CLOCKWISE: (Orientation.E, [
            ( 0,  0),
            ( 0, -1),
            (+1, -1),
            (-2,  0),
            (-2, -1),
        ]),
    },

    Orientation.E: {
        Command.COUNTERCLOCKWISE: (Orientation.N, [
            ( 0,  0),
            ( 0, +1),
            (-1, +1),
            (+2,  0),
            (+2, +1),
        ]),
        Command.CLOCKWISE: (Orientation.S, [
            ( 0,  0),
            ( 0, +1),
            (-1, +1),
            (+2,  0),
            (+2, +1),
        ]),
    },

    Orientation.S: {
        Command.COUNTERCLOCKWISE: (Orientation.E, [
            ( 0,  0),
            ( 0, -1),
            (+1, -1),
            (-2,  0),
            (-2, -1),
        ]),
        Command.CLOCKWISE: (Orientation.W, [
            ( 0,  0),
            ( 0, +1),
            (+1, +1),
            (-2,  0),
            (-2, +1),
        ]),
    },

    Orientation.W: {
        Command.COUNTERCLOCKWISE: (Orientation.S, [
            ( 0,  0),
            ( 0, -1),
            (-1, -1),
            (+2,  0),
            (+2, -1),
        ]),
        Command.CLOCKWISE: (Orientation.N, [
            ( 0,  0),
            ( 0, -1),
            (-1, -1),
            (+2,  0),
            (+2, -1),
        ]),
    },
}

ZBLOCK = {
    Orientation.N: {
        Command.COUNTERCLOCKWISE: (Orientation.W, [
            ( 0,  0),
            ( 0, +1),
            (+1, +1),
            (-2,  0),
            (-2, +1),
        ]),
        Command.CLOCKWISE: (Orientation.E, [
            ( 0,  0),
            ( 0, -1),
            (+1, -1),
            (-2,  0),
            (-2, -1),
        ]),
    },

    Orientation.E: {
        Command.COUNTERCLOCKWISE: (Orientation.N, [
            ( 0,  0),
            ( 0, +1),
            (-1, +1),
            (+2,  0),
            (+2, +1),
        ]),
        Command.CLOCKWISE: (Orientation.S, [
            ( 0,  0),
            ( 0, +1),
            (-1, +1),
            (+2,  0),
            (+2, +1),
        ]),
    },

    Orientation.S: {
        Command.COUNTERCLOCKWISE: (Orientation.E, [
            ( 0,  0),
            ( 0, -1),
            (+1, -1),
            (-2,  0),
            (-2, -1),
        ]),
        Command.CLOCKWISE: (Orientation.W, [
            ( 0,  0),
            ( 0, +1),
            (+1, +1),
            (-2,  0),
            (-2, +1),
        ]),
    },

    Orientation.W: {
        Command.COUNTERCLOCKWISE: (Orientation.S, [
            ( 0,  0),
            ( 0, -1),
            (-1, -1),
            (+2,  0),
            (+2, -1),
        ]),
        Command.CLOCKWISE: (Orientation.N, [
            ( 0,  0),
            ( 0, -1),
            (-1, -1),
            (+2,  0),
            (+2, -1),
        ]),
    },
}


SRS = {
    Tetramino.L: LBLOCK,
    Tetramino.J: JBLOCK,
    Tetramino.O: OBLOCK,
    Tetramino.I: IBLOCK,
    Tetramino.S: SBLOCK,
    Tetramino.Z: ZBLOCK,
    Tetramino.T: TBLOCK,
}