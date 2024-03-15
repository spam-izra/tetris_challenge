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

class Client:
    def __init__(self):
        pass

    def update(w, s) -> list[str]:
        """
            Implement in childs
        """
        return [Command.PASS.value]

    def loop(self):
        w = get_pkg()

        while True:
            s = get_pkg()
            cmd = self.update(w, s)
            put_pkg({
                "cmd": cmd,
            })


if __name__ == "__main__":
    c = Client()
    c.loop()