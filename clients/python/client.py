import sys
import os
import json
from enum import Enum


def get_pkg():
    with os.fdopen(sys.stdin.fileno(), "rb", closefd=False) as stdin:
        pkg_size = stdin.readline()
        pkg_size = int(pkg_size.decode("utf-8").strip())
        pkg_body = stdin.read(pkg_size)
        return json.loads(pkg_body.decode("utf-8"))

def put_pkg(obj):
    s = json.dumps(obj).encode("utf-8") + b'\n'
    with os.fdopen(sys.stdout.fileno(), "wb", closefd=False) as stdout:
        stdout.write(f"{len(s)}\n".encode("utf-8"))
        stdout.flush()
        stdout.write(s)
        stdout.flush()

class Command(Enum):
    PASS             = "P"
    SOFT_SPEEDUP     = "S"
    HARD_SPEEDUP     = "H"
    LEFT             = "L"
    RIGHT            = "R"
    CLOCKWISE        = "F"
    COUNTERCLOCKWISE = "B"

class Tetramino(Enum):
    O = "0"
    I = "1"
    T = "2"
    L = "3"
    J = "4"
    S = "5"
    Z = "6"

class Orientation(Enum):
    N = "0"
    E = "1"
    S = "2"
    W = "3"


class Sprite:
    def __init__(self, data) -> None:
        self.width = len(data[0])
        self.height = len(data)
        self.data = []
        for row in data:
            v = sum([ (1 << n)*v for n, v in enumerate(row)])
            self.data.append(v)

    def __repr__(self) -> str:
        s = f"[h {self.height} x w {self.width:d}]\n"
        for row in reversed(self.data):
            s += f'{row:08b}'[::-1].replace("0", " ")
            s += "\n"
        return s

class World:
    def __init__(self, js):
        self.width = js["width"]
        self.height = js["height"]
        self.content = []
        content = js["content"]
        for row in content:
            v = sum([ (1 << n)*v for n, v in enumerate(row)])
            self.content.append(v)

        sprites = js["sprites"]
        self.sprites = {}
        for t in sprites:
            t = Tetramino(t)
            self.sprites[t] = {}
            for ori in sprites[t.value]:
                ori = Orientation(ori)
                self.sprites[t][ori] = Sprite(sprites[t.value][ori.value])

        self.srs = {}
        srs = js["srs"]
        for t, tv in srs.items():
            t = Tetramino(t)
            for ori, oriv in tv.items():
                ori = Orientation(ori)
                for c, cv in oriv.items():
                    c = Command(c)
                    self.srs[(t, ori, c)] = Orientation(cv["to"]), cv["offsets"]

class Figure:
    def __init__(self, js) -> None:
        self.x = js["x"]
        self.y = js["y"]
        self.cell_y = js["cell_y"]
        self.next_y1 = js["next_y1"]
        self.next_y2 = js["next_y2"]
        self.figure = Tetramino(js["figure"])
        self.orientation = Orientation(js["orientation"])

    def __repr__(self) -> str:
        s = f'Fig(x={self.x} y={self.cell_y} f={self.figure.name} o={self.orientation.name})'
        return s

class State:
    def __init__(self, js) -> None:
        self.frame = js["frame"]
        self.score = js["score"]
        self.level = js["level"]
        self.lines = js["lines"]
        self.peek = [Tetramino(v) for v in js["peek"]]
        self.current_figure = None
        if js["current_figure"]:
            self.current_figure = Figure(js["current_figure"])
        self.content = []
        content = js["content"]
        for row in content:
            v = sum([ (1 << n)*v for n, v in enumerate(row)])
            self.content.append(v)

        self.speed1 = js["speed1"]
        self.speed2 = js["speed2"]

        pass

class Client:
    def __init__(self):
        pass

    def update(self, w: World, s: State) -> list[Command]:
        """
            Implement in childs
        """
        return [Command.PASS.value]

    def loop(self):
        w = get_pkg()
        world = World(w)

        while True:
            s = get_pkg()
            state = State(s)
            cmd = self.update(world, state)
            put_pkg({
                "cmd": [c.value for c in cmd],
            })


if __name__ == "__main__":
    c = Client()
    c.loop()