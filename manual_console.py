from tetrisim.state import TetrisEngine
from tetrisim.utils import parse_cmd
from tetrisim.commands import Command

s = TetrisEngine(seed=43)
print(s)

while not s.is_game_over:
    cmd = parse_cmd(input())
    if not cmd:
        cmd.append(Command.PASS)
    s.update(cmd=cmd)
    print(s)
