import sys
import os
import json
import random


DEBUG = True

def get_pkg():
    if DEBUG:
        f = open("log.txt", "a")
    else:
        f = None
    try:
        with os.fdopen(sys.stdin.fileno(), "rb", closefd=False) as stdin:
            pkg_size = stdin.readline()

            if f:
                print("pkg size: ", pkg_size, file=f)

            pkg_size = int(pkg_size.decode("utf-8").strip())
            pkg_body = stdin.read(pkg_size)
            if f:
                print("pkg body: ", pkg_body, file=f)

            return json.loads(pkg_body.decode("utf-8"))
    finally:
        if f is not None:
            f.close()


def put_pkg(obj):
    s = json.dumps(obj).encode("utf-8") + b'\n'
    with os.fdopen(sys.stdout.fileno(), "wb", closefd=False) as stdout:
        stdout.write(f"{len(s)}\n".encode("utf-8"))
        stdout.flush()
        stdout.write(s)
        stdout.flush()

world = get_pkg()

hard = False
while True:
    state = get_pkg()
    cmd = ["S"]
    shift = random.choice(["L", "R", None, None, None, None, None, None, None, None, None])
    if shift:
        cmd.append(shift)
    rotate = random.choice(["F", "B", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None])
    if rotate:
        cmd.append(rotate)
    put_pkg({
        "cmd": cmd,
    })
    hard = not hard