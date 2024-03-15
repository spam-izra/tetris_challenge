import random
from .tetramino import Tetramino
import base64

class Generator:
    def __init__(self, seed):
        self.seed = seed
        self.rng = random.Random(self.seed)
        self.history = []

        self.pool = [
            Tetramino.O,
            Tetramino.L,
            Tetramino.J,
            Tetramino.T,
            Tetramino.S,
            Tetramino.Z,
            Tetramino.I,
        ]

    def get(self, n: int) -> Tetramino:
        #return Tetramino.I
        while len(self.history) <= n:
            r = self.rng.choice(self.pool)
            self.history.append(r)
        return self.history[n]

def create_test_generator(t: Tetramino) -> Generator:
    class TestGen(Generator):
        def get(self, n: int) -> Tetramino:
            return t
    return TestGen