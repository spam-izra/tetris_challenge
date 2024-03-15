from .tetramino import Tetramino, Orientation
from .figure import Figure
from .commands import Command
from .state import TetrisEngine

TSPIN = 2
MINI_TSPIN = 1

class Tester:
    def __init__(self):
        self._cases = []

    def add_test(self, cmd, fig_before, map_before, fig_after, map_after, tspin=None):
        self._cases.append(
            (cmd, (fig_before, map_before), (fig_after, map_after), tspin),
        )

    def check(self):
        for n, c in enumerate(self._cases):
            r, msg = self.do(c)
            if not r:
                print("CASE", n, "= FAILED:", msg)
            else:
                print("CASE", n, "= OK")

    def do(self, c):
        cmd, before, after, tspin = c
        engine = TetrisEngine()
        engine.speed = lambda *, speedup=0: 0
        engine.set_map(before[1])
        engine.update(cmd=[Command.PASS])
        engine._current_figure = before[0]
        engine.update(cmd=cmd)
        #print(engine)

        if after[0].figure != engine._current_figure.figure:
            return False, "not same figure"
        if after[0].orientation != engine._current_figure.orientation:
            return False, "not same orientation" + str(engine._current_figure)

        if after[0].cell_x != engine._current_figure.cell_x or after[0].cell_y != engine._current_figure.cell_y:
            print(engine)
            return False, "not same pos" + str(engine._current_figure)

        engine._map.add_figure(engine._current_figure)
        for y, line in enumerate(after[1]):
            mline = list(engine._map.get_line(y))
            #print(mline)
            if list(line) != mline:
                return False, "not same map " + str(y) + str(line) + str(mline)

        return True, None

tester = Tester()

# I rotation
tester.add_test(
    cmd=[Command.CLOCKWISE],
    fig_before=Figure(Tetramino.I, Orientation.E, y=0, x=7),
    fig_after=Figure(Tetramino.I, Orientation.S, y=0, x=6),
    map_before=list(reversed([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])),
    map_after=list(reversed([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]))
)
tester.add_test(
    cmd=[Command.COUNTERCLOCKWISE],
    fig_before=Figure(Tetramino.I, Orientation.E, y=0, x=7),
    fig_after=Figure(Tetramino.I, Orientation.N, y=0, x=6),
    map_before=list(reversed([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])),
    map_after=list(reversed([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])),
)
tester.add_test(
    cmd=[Command.COUNTERCLOCKWISE],
    fig_before=Figure(Tetramino.I, Orientation.W, y=0, x=8),
    fig_after=Figure(Tetramino.I, Orientation.S, y=0, x=6),
    map_before=list(reversed([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])),
    map_after=list(reversed([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])),
)
tester.add_test(
    cmd=[Command.CLOCKWISE],
    fig_before=Figure(Tetramino.I, Orientation.E, y=0, x=7),
    fig_after=Figure(Tetramino.I, Orientation.S, y=2, x=6),
    map_before=list(reversed([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    ])),
    map_after=list(reversed([
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    ])),
)
tester.add_test(
    cmd=[Command.CLOCKWISE],
    fig_before=Figure(Tetramino.I, Orientation.W, y=0, x=8),
    fig_after=Figure(Tetramino.I, Orientation.N, y=1, x=6),
    map_before=list(reversed([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    ])),
    map_after=list(reversed([
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    ])),
)

# T Spin rotation
tester.add_test(
    cmd=[Command.CLOCKWISE],
    fig_before=Figure(Tetramino.T, Orientation.E, y=0, x=3),
    fig_after=Figure(Tetramino.T, Orientation.S, y=0, x=3),
    map_before=list(reversed([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    ])),
    map_after=list(reversed([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    ])),
    tspin=TSPIN,
)
tester.add_test(
    cmd=[Command.CLOCKWISE],
    fig_before=Figure(Tetramino.T, Orientation.S, y=0, x=3),
    fig_after=Figure(Tetramino.T, Orientation.W, y=0, x=3),
    map_before=list(reversed([
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    ])),
    map_after=list(reversed([
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    ])),
    tspin=TSPIN,
)
tester.add_test(
    cmd=[Command.COUNTERCLOCKWISE],
    fig_before=Figure(Tetramino.T, Orientation.N, y=2, x=4),
    fig_after=Figure(Tetramino.T, Orientation.W, y=0, x=5),
    map_before=list(reversed([
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 1, 0, 0],
    ])),
    map_after=list(reversed([
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    ])),
    tspin=TSPIN,
)
tester.add_test(
    cmd=[Command.CLOCKWISE],
    fig_before=Figure(Tetramino.T, Orientation.N, y=2, x=3),
    fig_after=Figure(Tetramino.T, Orientation.E, y=0, x=2),
    map_before=list(reversed([
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 1, 1, 1, 0, 0],
    ])),
    map_after=list(reversed([
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    ])),
    tspin=TSPIN,
)
tester.add_test(
    cmd=[Command.CLOCKWISE],
    fig_before=Figure(Tetramino.T, Orientation.N, y=0, x=0),
    fig_after=Figure(Tetramino.T, Orientation.E, y=0, x=-1),
    map_before=list(reversed([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    ])),
    map_after=list(reversed([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    ])),
    tspin=MINI_TSPIN,
)
tester.add_test(
    cmd=[Command.CLOCKWISE],
    fig_before=Figure(Tetramino.T, Orientation.N, y=0, x=2),
    fig_after=Figure(Tetramino.T, Orientation.E, y=0, x=1),
    map_before=list(reversed([
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    ])),
    map_after=list(reversed([
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    ])),
    tspin=MINI_TSPIN,
)
tester.add_test(
    cmd=[Command.CLOCKWISE],
    fig_before=Figure(Tetramino.T, Orientation.W, y=0, x=2),
    fig_after=Figure(Tetramino.T, Orientation.N, y=-1, x=1),
    map_before=list(reversed([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 1, 1, 1, 1, 0],
    ])),
    map_after=list(reversed([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    ])),
    tspin=MINI_TSPIN,
)

tester.check()