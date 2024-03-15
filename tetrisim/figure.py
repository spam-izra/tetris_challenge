
from .tetramino import Orientation, Sprites, Tetramino
from .commands import Command
from .srs import SRS
import math

class Figure:
    def __init__(self, figure: Tetramino, orientation: Orientation, *, x: int, y: float):
        assert isinstance(x, int)
        assert isinstance(y, (int, float))
        assert isinstance(figure, Tetramino)
        assert isinstance(orientation, Orientation)

        self.__figure = figure
        self.__orientation = orientation
        self.__x = x
        self.__y = y

    @property
    def figure(self): return self.__figure

    @property
    def orientation(self): return self.__orientation

    @property
    def cell_x(self): return self.__x

    @property
    def cell_y(self): return math.floor(self.__y)

    @property
    def y(self): return self.__y

    @property
    def cell_pos(self): return self.cell_y, self.cell_x

    def sprite(self) -> list[list[int]]:
        return Sprites[self.__figure][self.__orientation]

    def __repr__(self):
        return f'Fig({str(self.__figure.name)}, {self.__orientation.name}, x={self.__x}, y={self.__y} [{self.cell_y}])'

    # Action

    def rotate(self, command: Command) -> list["Figure"]:
        ori, offsets = SRS[self.__figure][self.__orientation][command]

        return [
            Figure(figure=self.__figure, orientation=ori,
                   x=self.__x + dx, y=self.__y + dy)
            for dy, dx in offsets
        ]

    def offset(self, *, dy: float = 0.0, dx: int = 0) -> "Figure":
        return Figure(
            figure=self.figure, orientation=self.orientation,
            x=self.__x + dx, y=self.__y + dy)

    def to_pos(self, *, x: int=None, y: float=None) -> "Figure":
        return Figure(
            figure=self.figure, orientation=self.orientation,
            x=self.__x if x is None else x, y=self.__y if y is None else y)


