from .commands import Command


def parse_cmd(cmd: str) -> list[Command]:
    return [Command(c) for c in cmd]

def validate_cmd(cmd: list[Command]):
    cmd = cmd[:]
    if len(cmd) == 0:
        return False

    if len(cmd) == 1 and cmd[0] in [Command.PASS, Command.HARD_SPEEDUP]:
        return True


    if Command.RIGHT in cmd and Command.LEFT in cmd:
        return False
    if Command.CLOCKWISE in cmd and Command.COUNTERCLOCKWISE in cmd:
        return False

    for v in [
        Command.LEFT, Command.RIGHT,
        Command.CLOCKWISE, Command.COUNTERCLOCKWISE,
        Command.SOFT_SPEEDUP]:
        if v in cmd:
            cmd.remove(v)

    return len(cmd) == 0