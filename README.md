# Tetris Engine

## Requirements

It use `Dear ImGui` for debug view.

```
git clone https://github.com/spam-izra/tetris_challenge.git
cd tetris_challenge
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python manual_console.py or python manual_gui.py
```

## Tetris Simulator

Module `tetrisim` allow to simulate behaviour of tetris game without any gui. It suppose that the game process player inputs each frame and thera are only 30 frames per second.

Example:
```
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
```

Each frame you must send user input or send PASS if there is no any one. There are the following commands
* `R` - move right
* `L` - move left
* `F` - clockwise rotation
* `B` - counterclockwise rotation
* `P` - pass (it does not allow other commands)
* `S` - speedup
* `H` - drop figure and fix it (it does not allow other commands)

Each user input may content only one rotation and one move commands. Commands will apply to figure in begin of the frame accoring to order in command list.


## Bot Runner

It has runner for any AI clients. You need just edit `settings.json` and run script
```
python runner.py
```

Example of AI client can be found in `client_example.py`.
