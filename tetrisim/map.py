
from .figure import Figure

class Map:
    def __init__(self, width: int, height: int) -> None:
        self.__border = 5
        self.__width = width
        self.__height = height

        self.__map =  [
            (
                [1 for _ in range(self.border)] +
                [1 for _ in range(self.width)] +
                [1 for _ in range(self.border)]
            ) for _ in range(self.border)
        ] + [
            (
                [1 for _ in range(self.border)] +
                [0 for _ in range(self.width)] +
                [1 for _ in range(self.border)]
            ) for _ in range(max(self.height * 2, self.border*2)) # we add some buffer upon map
        ]

    @property
    def border(self): return self.__border

    @property
    def width(self): return self.__width

    @property
    def height(self): return self.__height

    @property
    def size(self): return self.height, self.width

    def get_cell(self, y: int, x: int) -> int:
        return self.__map[self.border + y][self.border + x]

    def set_cell(self, y: int, x: int, value: int):
        self.__map[self.border + y][self.border + x] = value

    def get_line(self, y: int) -> list[int]:
        return self.__map[self.border + y][self.border:self.border + self.width]

    def set_line(self, y:int, line: list[int]):
        assert len(line) == self.width
        for x, v in enumerate(line):
            self.set_cell(y, x, v)

    def has_collision(self, figure: Figure) -> bool:
        sprite = figure.sprite()
        y, x = figure.cell_pos

        for fy, row in enumerate(sprite):
            my = y + fy
            for fx, v in enumerate(row):
                mx = x + fx
                if v == 1 and self.get_cell(my, mx) == 1:
                    return True
        return False

    def add_figure(self, figure: Figure):
        sprite = figure.sprite()
        y, x = figure.cell_pos

        for fy, row in enumerate(sprite):
            my = y + fy
            for fx, v in enumerate(row):
                mx = x + fx
                if v == 1:
                    assert self.get_cell(my, mx) == 0
                    self.set_cell(my, mx, 1)