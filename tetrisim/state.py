from .gen import Generator
from .tetramino import Sprites, Orientation, Tetramino, START_POSITION
from .srs import SRS
from enum import Enum
from .figure import Figure
from .map import Map
from .utils import validate_cmd
from .commands import Command
import json

PEEK=1
SHIFT_THR = 2
LOCK_TIMER = 15
SOFT_SPEEDUP_MULTIPLICATOR = 20

class State (Enum) :
    IDLE    = 0
    FALLING = 1
    LOCKING = 2
    OVER    = 3


class TSPIN (Enum):
    NONE = 0
    MINI = 1
    FULL = 2
    FULL_LAST_POINT = 4


class TetrisEngine:
    """
        Simple tetris engine for 30 fps.
        x direction is left-to-right
        y direction is bottom-to-up
    """
    def __init__(self, width: int = 10, height: int = 20, *, seed: int = None, GeneratorFabric=Generator):
        assert width > 0
        assert height > 0

        # base config
        self._map = Map(width, height)
        self._gen = GeneratorFabric(seed=seed)

        # dynamic states
        self._frame = 0
        self._score = 0
        self._lines = 0
        self._current_figure_index = 0
        self._current_figure = None
        self._state = State.IDLE
        self._b2b_state = False

        self._lock_timer = 0
        self._rotation_state = None
        self._is_last_rotation_point = False
        self._hard_state = None
        self._shift_state = None
        self._shift_counter = 0
        self._speedup_counter = 0
        self._min_falling_y = None

        # last action, it will be reseted with new action or figure moving.
        self._last_action = None
        self._tspin = TSPIN.NONE

    @property
    def is_game_over(self): return self._state == State.OVER

    @property
    def level(self):
        """
            Calculate current level accoring number or removed lines.
        """
        value = self._lines // 10 + 1
        return min(value, 15)

    @property
    def score(self):
        return self._score

    def set_map(self, values: list[list[int]]):
        """
            Set current state of map

            values is sequence of rows from bottom to up.
        """

        for y in range(self._map.height + self._map.border):
            for x in range(self._map.width):
                self._map.set_cell(y, x, 0)

        for y, row in enumerate(values):
            for x, value in enumerate(row):
                self._map.set_cell(y, x, value)

    def peek_next(self, count=1) -> list[Tetramino]:
        return [
            self._gen.get(self._current_figure_index + 1 + i) for i in range(0, count)
        ]

    def speed(self, speedup=False) -> float:
        """
        Calculate speed of falling according to current level
        """
        v = 1.0 / ( 0.8 - 0.007 * (self.level - 1) ) ** (self.level - 1) / 30
        if not speedup:
            return v
        else:
            return v * SOFT_SPEEDUP_MULTIPLICATOR

    def update(self, cmd: list[Command]):
        """
            Update tetris state using list of commands

            L - left shift
            R - right shift
            H - hard speedup
            S - soft speedup
            F - rotate clockwise
            B - rotate counterclockwise
            P - pass

            Allowed only on rotate or horizontal shift directions.

            H and P are exclusive and does't allow any other commands in list.
        """

        assert validate_cmd(cmd), "Invalid commands"

        if self._state == State.IDLE:
            self.__handle_idle()
        elif self._state == State.FALLING:
            self.__handle_falling(cmd)
        elif self._state == State.LOCKING:
            self.__handle_locking(cmd)
            # After commands there is some chance that figure can start to fall again
            if self._state == State.FALLING:
                self.__handle_falling(cmd=[Command.PASS])

        # Check endgame condition
        if any(self._map.get_line(self._map.height)):
            self._state = State.OVER
            self._current_figure = None

        # update inner timers
        self.__update_timers()

    def __repr__(self):
        s = ""
        s += "=" * 80 + "\n"

        SW = 80
        SH = 28
        screen = [
            [' ' for _ in range(SW)] for _ in range(SH)
        ]

        def apply(y, x, line):
            cy = SH - y - 1
            if cy < 0 or cy >= len(screen):
                return

            for i, v in enumerate(line):
                cx = x + i
                if cx >= SW: continue
                screen[cy][cx] = v

        for y in range(self._map.height + 2, 0, -1):
            line = "".join(
                "O" if v == 1 else " "
                for v in self._map.get_line(y - 1)
            )
            apply(y + 3, 0, f'{y-1:2d} |' + line + "|")

        apply(3, 0, f'   +' + self._map.width * "-" + "+")

        apply(23, 17, f'Frame: {self._frame:8d}')
        apply(22, 17, f'Score: {self._score:8d}')
        apply(21, 17, f'Next : {"UNK" if self.peek_next(PEEK) is None else str([v.name for v in self.peek_next(PEEK)]):>8s}')
        apply(20, 17, f'Level: {self.level:8d}')
        apply(19, 17, f'Speed: {self.speed():8.3f}')
        apply(18, 17, f'State: {self._state.name:>8s}')
        apply(17, 17, f'Timer: {self._lock_timer:8d}')
        apply(16, 17, f'Act  : {str(self._last_action):>8s}')

        apply(15, 17, f'RoSta: {str(self._rotation_state):>8s}')
        apply(14, 17, f'HrSta: {str(self._hard_state):>8s}')
        apply(13, 17, f'ShSta: {str(self._shift_state):>8s}')
        apply(12, 17, f'ShCou: {str(self._shift_counter):>8s}')
        apply(11, 17, f'SpCou: {str(self._speedup_counter):>8s}')

        apply(9, 17,  f'B2B  : {str(self._b2b_state):>8s}')
        apply(9, 17,  f'TSPIN: {str(self._tspin.name):>8s}')

        if self._current_figure:
            sprite = self._current_figure.sprite()
            for y, row in enumerate(sprite):
                for x, v in enumerate(row):
                    if v == 0:
                        continue
                    apply(y + 3 + 1 + self._current_figure.cell_y,
                          x + 4 + self._current_figure.cell_x,
                          "#")

        for row in screen:
            s += "".join(row) + "\n"

        s += str(self._current_figure) + "\n"
        s += "=" * 80 + "\n"

        return s

    def __update_timers(self):
        self._lock_timer = max(0, self._lock_timer - 1)
        self._frame += 1
        self._shift_counter = max(0, self._shift_counter - 1)

    def __handle_idle(self):
        """
            Init new figure appearance
        """
        assert self._current_figure is None

        # get new figure
        self._current_figure_index += 1
        next_tetramino = self._gen.get(self._current_figure_index)

        # start position
        x_start = self._map.width // 2 - 2
        y_start = self._map.height

        # offset from start position
        dy, dx = START_POSITION[next_tetramino]

        self._current_figure = Figure(
            figure=next_tetramino,
            orientation=Orientation.N,
            x = x_start + dx,
            y = y_start + dy,
        )
        self._min_falling_y = self._current_figure.y

        # resetting inner state
        self._lock_timer = 0
        self._rotation_state = None
        # the only state that must keeping
        #self._hard_state = None
        self._shift_state = None
        self._shift_counter = 0
        self._speedup_counter = 0
        self._last_action = None
        self._tspin = TSPIN.NONE

        # new state of engine
        self._state = State.FALLING

    def __handle_falling(self, cmd: list[Command]):
        """
            Handle falling state.
            The first step is to handle user commands. Commands apply one by one according order in list.
        """
        self.__handle_command(cmd)

        # if we are still falling
        if self._state == State.FALLING:
            old_min_y = self._min_falling_y
            speedup = Command.SOFT_SPEEDUP in cmd

            self.__apply_speed(speedup=speedup)
            self._min_falling_y = min(self._min_falling_y, self._current_figure.y)
            if speedup:
                self._speedup_counter += max(old_min_y - self._min_falling_y, 0)

            self.__speedup_score()
            # reset last action if figure moving
            if self._last_action is not None and self._last_action[0] != self._current_figure.cell_y:
                self._last_action = None
                self._tspin = TSPIN.NONE

    def __handle_locking(self, cmd):
        """
            Handle behaviour of figure on surface.
        """
        self.__handle_command(cmd)

        if self._state != State.LOCKING:
            return

        # it is possible falling again as result of command application
        if not self._map.has_collision(self._current_figure.to_pos(y=self._current_figure.cell_y - 1)):
            self._state = State.FALLING
            return

        if self._lock_timer > 0:
            return

        self._map.add_figure(self._current_figure)
        self.__clear_lines()
        self._state = State.IDLE
        self._current_figure = None

    def __speedup_score(self):
        while self._speedup_counter >= 1.0:
            self._score += 1
            self._speedup_counter -= 1

    def __apply_speed(self, speedup: bool):
        """
            Apply current speed to current figure.
        """
        s = self.speed(speedup=speedup)

        tmp_figure = self._current_figure.offset(dy=-s)
        # no moving
        if tmp_figure.cell_y == self._current_figure.cell_y:
            self._current_figure = tmp_figure
            return

        for y in reversed(range(tmp_figure.cell_y, self._current_figure.cell_y)):
            tmp = self._current_figure.to_pos(y=y)

            # if we have collision then we should stop falling and begin locking
            if self._map.has_collision(tmp):
                # put on previous y
                self._current_figure = self._current_figure.to_pos(y=y+1)
                self._state = State.LOCKING
                self._lock_timer = LOCK_TIMER
                return
        self._current_figure = tmp_figure

    def __check_tspin(self):
        if self._current_figure.figure != Tetramino.T:
            self._tspin = TSPIN.NONE
            return

        rect = self._map.get_cell(
            self._current_figure.cell_y + 1,
            self._current_figure.cell_x
        ) + self._map.get_cell(
            self._current_figure.cell_y + 1,
            self._current_figure.cell_x + 2
        ) + self._map.get_cell(
            self._current_figure.cell_y,
            self._current_figure.cell_x + 1
        ) + self._map.get_cell(
            self._current_figure.cell_y + 2,
            self._current_figure.cell_x + 1
        )

        angle = self._map.get_cell(
            self._current_figure.cell_y,
            self._current_figure.cell_x
        ) + self._map.get_cell(
            self._current_figure.cell_y,
            self._current_figure.cell_x + 2
        ) + self._map.get_cell(
            self._current_figure.cell_y + 2,
            self._current_figure.cell_x
        ) + self._map.get_cell(
            self._current_figure.cell_y + 2,
            self._current_figure.cell_x + 2
        )

        has_slot = (angle >= 3 and rect <= 1)
        if not has_slot:
            self._tspin = TSPIN.NONE
            return

        check_point = {
            Orientation.N: [(2, 0), (2, 2)],
            Orientation.E: [(0, 2), (2, 2)],
            Orientation.S: [(0, 0), (0, 2)],
            Orientation.W: [(0, 0), (2, 0)],
        }

        counter = 0
        for dy, dx in check_point[self._current_figure.orientation]:
            counter += self._map.get_cell(
                self._current_figure.cell_y + dy,
                self._current_figure.cell_x + dx)

        assert counter > 0
        if counter == 2:
            if self._tspin != TSPIN.FULL_LAST_POINT:
                self._tspin = TSPIN.FULL_LAST_POINT if self._is_last_rotation_point else TSPIN.FULL
        else:
            if self._tspin != TSPIN.FULL_LAST_POINT:
                self._tspin = TSPIN.FULL_LAST_POINT if self._is_last_rotation_point else TSPIN.MINI

        print("TSPIN!", self._tspin)

    def __handle_command(self, cmd: list[Command]):
        """
            We suppose that cmd is valid
        """

        # Reset rotation state in case of absent rotation command
        if Command.CLOCKWISE not in cmd and Command.COUNTERCLOCKWISE not in cmd:
            self._rotation_state = None

        # Same for shift commands
        if Command.LEFT not in cmd and Command.RIGHT not in cmd:
            self._shift_state = None
            self._shift_counter = 0

        # And for hard speedup
        if Command.HARD_SPEEDUP not in cmd:
            self._hard_state = None

        if cmd[0] == Command.HARD_SPEEDUP:
            self.__do_hard_drop()
            return

        if cmd[0] == Command.PASS:
            if self._shift_state is not None:
                self.__do_shift(self._shift_state)
            return

        action = []
        for c in cmd:
            if c == Command.LEFT:
                if self.__do_shift(-1):
                    action.append(c)
            elif c == Command.RIGHT:
                if self.__do_shift(+1):
                    action.append(c)
            if c == Command.CLOCKWISE:
                if self.__do_rotate(c):
                    action.append(c)
            elif c == Command.COUNTERCLOCKWISE:
                if self.__do_rotate(c):
                    action.append(c)

        if action:
            self._last_action = (self._current_figure.cell_y, action)
            if Command.CLOCKWISE in action or Command.COUNTERCLOCKWISE in action:
                self.__check_tspin()

    def __do_hard_drop(self):
        # do nothing if hard state was not resetted
        if self._hard_state:
            return
        self._hard_state = Command.HARD_SPEEDUP

        # Moving figure to down
        tmp_figure = self._current_figure.offset()
        while not self._map.has_collision(tmp_figure.offset(dy=-1)):
            self._score += 2
            tmp_figure = tmp_figure.offset(dy=-1)

        # if it moved we reset last action state
        if tmp_figure.cell_y != self._current_figure.cell_y:
            self._last_action = None
            self._tspin = TSPIN.NONE

        self._current_figure = tmp_figure
        self._map.add_figure(self._current_figure)
        self._state = State.IDLE
        self._current_figure = None

        # clear lines and score
        self.__clear_lines()

    def __do_rotate(self, direction):
        """
            Make rotation. It will return True if real rotation occurs.
        """

        # We can rotate only after resetting rotation state.
        # Rotation state is resetted in case of direction change or
        # no rotation command.
        if self._rotation_state is not None and self._rotation_state == direction:
            return False

        self._rotation_state = direction

        tmp_figures = self._current_figure.rotate(direction)
        for n, f in enumerate(tmp_figures):
            if self._map.has_collision(f):
                continue

            #print(f"ROT [{self._current_figure.figure.name}] {self._current_figure.orientation.name} => {f.orientation.name} around {n + 1}" )

            self._current_figure = f
            self._is_last_rotation_point = (len(tmp_figures) - 1 == n)
            return True

        return False

    def __do_shift(self, dx) -> False:
        """
            Make horizontal shift. It will return True if real shift occurs
        """

        # reset shift state if direction was changed
        if self._shift_state != dx:
            self._shift_state = dx
            self._shift_counter = 0

        # tick-tack horizontal shift
        if self._shift_counter != 0:
            return False

        self._shift_counter = SHIFT_THR
        tmp_figure = self._current_figure.offset(dx=self._shift_state)
        if self._map.has_collision(tmp_figure):
            return False

        self._current_figure = tmp_figure
        return True

    def __clear_lines(self):
        counter = 0
        # remove lines
        for y in range(self._map.height, -1, -1):
            line = self._map.get_line(y)
            if all(self._map.get_line(y)):
                counter += 1
                for ny in range(y + 1, 2 * self._map.height):
                    self._map.set_line(ny - 1, self._map.get_line(ny))

        # scoring
        if counter == 4:
            m = 1.5 if self._b2b_state else 1.0
            self._b2b_state = True
            self._score += int(self.level * 800 * m)
        elif counter == 3:
            if self._tspin == TSPIN.MINI:
                assert False, "IMPOSSIBLE MINI TSPIN DOUBLE LINE"
            elif self._tspin == TSPIN.FULL or self._tspin == TSPIN.FULL_LAST_POINT:
                m = 1.5 if self._b2b_state else 1.0
                self._b2b_state = True
                self._score += int(self.level * 1600 * m)
            else:
                self._b2b_state = False
                self._score += self.level * 500
        elif counter == 2:
            if self._tspin == TSPIN.MINI:
                assert False, "IMPOSSIBLE MINI TSPIN DOUBLE LINE"
            elif self._tspin == TSPIN.FULL or self._tspin == TSPIN.FULL_LAST_POINT:
                m = 1.5 if self._b2b_state else 1.0
                self._b2b_state = True
                self._score += int(self.level * 1200 * m)
            else:
                self._b2b_state = False
                self._score += self.level * 300
        elif counter == 1:
            if self._tspin == TSPIN.MINI:
                m = 1.5 if self._b2b_state else 1.0
                self._b2b_state = True
                self._score += int(self.level * 200 * m)
            elif self._tspin == TSPIN.FULL or self._tspin == TSPIN.FULL_LAST_POINT:
                m = 1.5 if self._b2b_state else 1.0
                self._b2b_state = True
                self._score += int(self.level * 800 * m)
            else:
                self._b2b_state = False
                self._score += self.level * 100
        elif counter == 0:
            if self._tspin == TSPIN.MINI:
                self._score += self.level * 100
            elif self._tspin == TSPIN.FULL or self._tspin == TSPIN.FULL_LAST_POINT:
                self._score += self.level * 400
        else:
            assert False

        self._lines += counter



