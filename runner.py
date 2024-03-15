import json
import sys
import os
import time
from tetrisim.state import TetrisEngine, State
from tetrisim.figure import Sprites, Tetramino, Orientation
from tetrisim.srs import SRS
from tetrisim.commands import Command
from tetrisim.utils import parse_cmd
from utils import Application

from subprocess import Popen, PIPE
import threading
import queue
import imgui


def enqueue_stream(stream, queue):
    while True:
        b = stream.readline()
        if b == b'':
            stream.close()
            return
        s = int(b.decode("utf-8").strip())

        b = stream.read(s)
        if b == b'':
            stream.close()
            return

        body = b.decode("utf-8")
        queue.put(json.loads(body))


class Runner:
    def __init__(self, *, cfg) -> None:
        self.cfg = cfg
        self.engine = TetrisEngine(width=cfg["map"]["width"], height=cfg["map"]["height"], seed=self.cfg["seed"])
        content = cfg["map"]["content"]
        self.engine.set_map(content)

        self.queue = queue.Queue(10)
        self.p = Popen(self.cfg["client"]["cmd"], stdin=PIPE, stdout=PIPE)
        self.to = threading.Thread(target=enqueue_stream, args=(self.p.stdout, self.queue))
        self.to.start()

    def dispose(self):
        self.p.kill()
        self.p.stdout.close()
        self.to.join()

    def init_client(self):
        world = self.prepare_world()
        self.send(world, self.p.stdin)

    def do(self):
        if self.engine._state == State.OVER:
            return

        self.send(self.prepare_state(), self.p.stdin)
        cmd = self.get()
        #print("OUT:", cmd)

        cmd = parse_cmd("".join(cmd["cmd"]))
        self.engine.update(cmd)
        if self.engine._state == State.OVER:
            print("GAME OVER", self.engine.score)
        #print(self.engine)

    def prepare_world(self):
        obj = {
            "width": self.engine._map.width,
            "height": self.engine._map.height,
            "content": [],
            "sprites": {},
            "srs": {},
        }

        for y in range(0, self.engine._map.height):
            obj["content"].append(self.engine._map.get_line(y))

        for fig in Tetramino:
            obj["sprites"][fig.value] = {}
            for ori in Orientation:
                obj["sprites"][fig.value][ori.value] = Sprites[fig][ori]

        for fig in Tetramino:
            obj["srs"][fig.value] = {}
            for ori in Orientation:
                obj["srs"][fig.value][ori.value] = {
                    Command.CLOCKWISE.value: {
                        "to": str(SRS[fig][ori][Command.CLOCKWISE][0].value),
                        "offsets": SRS[fig][ori][Command.CLOCKWISE][1],
                    },
                    Command.COUNTERCLOCKWISE.value: {
                        "to": str(SRS[fig][ori][Command.COUNTERCLOCKWISE][0].value),
                        "offsets": SRS[fig][ori][Command.COUNTERCLOCKWISE][1],
                    },
                }

        return obj

    def prepare_state(self):
        obj = {
            "frame": self.engine._frame,
            "score": self.engine._score,
            "level": self.engine.level,
            "lines": self.engine._lines,
            "peek": [str(self.engine.peek_next(1)[0].value)],
            "current_figure": None,
            "content": [],

        }
        speed1 = self.engine.speed(False)
        obj["speed1"] = speed1
        speed2 = self.engine.speed(True)
        obj["speed2"] = speed2
        if self.engine._current_figure:
            obj["current_figure"] = {
                "x": self.engine._current_figure.cell_x,
                "y": self.engine._current_figure.y,
                "cell_y": self.engine._current_figure.cell_y,
                "next_y1": self.engine._current_figure.cell_y + speed1,
                "next_y2": self.engine._current_figure.cell_y + speed2,
                "figure": str(self.engine._current_figure.figure.value),
                "orientation": str(self.engine._current_figure.orientation.value),
            }

        for y in range(0, self.engine._map.height):
            obj["content"].append(self.engine._map.get_line(y))

        return obj

    def send(self, obj, stdin):
        s = json.dumps(obj).encode("utf-8") + b'\n'
        stdin.write(f'{len(s)}\n'.encode("utf-8"))
        stdin.write(s)
        stdin.flush()

    def get(self):
        t = time.monotonic()
        while True:
            try:
                obj = self.queue.get(timeout=1/30)
            except queue.Empty:
                dt = time.monotonic() - t
                if dt < 1/30:
                    print("TOO EARLY")
                    continue

            dt = time.monotonic() - t
            if dt > 1/30:
                raise TimeoutError
            return obj

    def loop(self):
        while self.engine._state != State.OVER:
            self.do()

        print("GAME OVER:", self.engine.score)



class MyApp(Application, Runner):
    def __init__(self, *, screen_size=(800, 720), title="Tetris", cfg):
        Application.__init__(self, screen_size=screen_size, title=title)
        Runner.__init__(self, cfg=cfg)

    def draw(self, dt: float, width: int, height: int, keys):
        self.do()
        with imgui.begin("Tetris"):
            imgui.text(str(self.engine))

if __name__ == "__main__":
    fpath = sys.argv[1] if len(sys.argv) > 1 else "setting.json"
    cfg = json.load(open(fpath))

    if cfg["gui"]:
        r = MyApp(cfg=cfg)
    else:
        r = Runner(cfg=cfg)

    try:
        r.init_client()
        r.loop()
    except Exception as e:
        print("ERROR", type(e), e.args)
    finally:
        r.dispose()
