from shlex import split as shlex
import argparse
import os.path
from os import environ
import readline


parser = argparse.ArgumentParser(
    prog="SAFE: Slow As F**k Editor",
    description="Edit files in a shell-like environment to make editing slower",
)

parser.add_argument(
    "filename",
    default="",
    nargs="?",
    help="filename to open, leave blank to create new file",
)
parser.add_argument(
    "-s", "--script", help="Lets you run a script to edit files automatically."
)


def listinsert(list, ins_index, obj):
    llen = len(list)
    if ins_index > llen:
        for i in range(llen, ins_index - 1):
            list.insert(i, "")
        list.insert(ins_index - 1, obj)
    else:
        list.insert(ins_index, obj)
    return list


# to anyone reading this: please make a PR for environment variables for the script functionality im too lazy

args = parser.parse_args()
if args.filename == "":
    buffer = [""]
elif not os.path.exists(args.filename):
    buffer = [""]
else:
    with open(args.filename, "r") as f:
        buffer = str(f.read()).split("\n")

filename = args.filename
savestatus = "  "
debugmode = False

readline.set_history_length(10)


def run_cmd(line):
    global filename, debugmode
    line = shlex(line)
    line[0] = line[0].lower()
    if line[0] == "edit":
        buffer[int(line[1]) - 1] = line[2]
        savestatus = "* "
    elif line[0] == "insert":
        listinsert(buffer, int(line[1]), line[2])
        savestatus = "* "
    elif line[0] == "delete":
        if len(line) > 2:
            for i in range(int(line[1]), int(line[2])):
                buffer.pop(i)
        else:
            buffer.pop(int(line[1]))
        savestatus = "* "
    elif line[0] == "cat":
        for l, i in enumerate(buffer):
            print(str(l + 1), i)
    elif line[0] == "cls" or line[0] == "clear":
        print("\033c", end="")
    elif line[0] == "save":
        if filename == "":
            print("No Filename Specified. Set it using setfilename command")
        else:
            with open(filename, "w") as f:
                f.write("\n".join(buffer))
            savestatus = "  "
    elif line[0] == "setfilename":
        filename = line[1]
    elif line[0] == "debug":
        debugmode = not debugmode
    elif line[0] == "exit":
        exit()
    elif line[0] == "info":
        if not filename == "" and os.path.exists(filename):
            print(
                f"Last Modified: {os.path.getmtime(filename)}\nSize In Bytes: {os.path.getsize(filename)}"
            )
    else:
        print("Command not recognized!")


if not args.script:
    while 1:
        try:
            line = input(f"{savestatus}{filename if filename != '' else 'unnamed'} $ ")
            readline.add_history(line)
            run_cmd(line)
        except KeyboardInterrupt as e:
            print('\nCtrl+C pressed, please use "exit" command to quit.')
        except Exception as e:
            if debugmode:
                import traceback

                traceback.print_exc()
            else:
                print(e)

else:
    script = open(args.script, "r").read()
    for i in str(script).split("\n"):
        run_cmd(i)
    run_cmd("save")
    run_cmd("exit")
