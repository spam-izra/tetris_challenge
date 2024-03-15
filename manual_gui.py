from imgui.integrations.glfw import GlfwRenderer
import OpenGL.GL as gl
import glfw
import imgui

import time
import sys

from tetrisim.state import TetrisEngine
from tetrisim.commands import Command
from tetrisim.gen import create_test_generator
from tetrisim.figure import Tetramino

from utils import Application
from test import *

TEST1 = (
    Tetramino.T,
    list(reversed([
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 1, 1, 0, 1, 0, 0, 0,],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0,],
    ]))
)
TEST2 = (
    Tetramino.T,
    list(reversed([
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0,],
    ]))
)
TEST3 = (
    Tetramino.T,
    list(reversed([
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0,],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0,],
        [0, 1, 1, 0, 1, 1, 1, 0, 0, 0,],
        [0, 1, 0, 0, 0, 1, 1, 1, 0, 0,],
        [0, 1, 0, 0, 1, 1, 1, 1, 1, 0,],
        [0, 1, 0, 0, 1, 1, 1, 1, 1, 0,],
    ]))
)

class MyApp(Application):
    def __init__(self, *, screen_size=(800, 720), title="Application"):
        super().__init__(screen_size=screen_size, title=title)

        self.engine = TetrisEngine(seed=42)

        #f, map = TEST3
        #self.engine = TetrisEngine(seed=42, GeneratorFabric=create_test_generator(f))
        #self.engine.set_map(map)

    def draw(self, dt: float, width: int, height: int, keys):
        cmd = []

        if "A" in keys:
            cmd.append(Command.LEFT)
        elif "D" in keys:
            cmd.append(Command.RIGHT)

        if "Q" in keys:
            cmd.append(Command.COUNTERCLOCKWISE)
        elif "E" in keys:
            cmd.append(Command.CLOCKWISE)

        if "S" in keys:
            cmd.append(Command.SOFT_SPEEDUP)

        if "W" in keys:
            cmd.append(Command.HARD_SPEEDUP)

        if not cmd:
            cmd.append(Command.PASS)

        self.engine.update(cmd)
        with imgui.begin("Tetris"):
            imgui.text(str(self.engine))
            imgui.text("\nCMD: " + str(cmd))
            imgui.text("\nKEYS: " + str(keys))

def main():
    app = MyApp()
    app.loop()

if __name__ == "__main__":
    main()


