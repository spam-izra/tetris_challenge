import sys
import os
import json
import random

from clients.python.client import *

class MyBot(Client):
    def __init__(self):
        super().__init__()

    def update(self, w, s) -> list[Command]:
        assert w.width == 10
        return [Command.PASS]


if __name__ == "__main__":
    c = MyBot()
    c.loop()