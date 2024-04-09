from shlex import split as shlex
import argparse

#! Current Name: Slow As Fuck Editor / SAFE

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

args = parser.parse_args()
print(args.filename)
if args.filename == "":
    buffer = [""]
else:
    with open(args.filename, "r") as f:
        buffer = str(f.read()).split("\n")

filename = args.filename
savestatus = ""

while 1:
    try:
        line = input(f"{savestatus} {filename if filename != '' else 'unnamed'} $ ")
        line = shlex(line)
        line[0] = line[0].lower()
        if line[0] == "edit":
            buffer[int(line[1])] = line[2]
            savestatus = '*'
        if line[0] == "insert":
            buffer.insert(int(line[1]), line[2])
            savestatus = '*'
        if line[0] == "cat":
            for l, i in enumerate(buffer):
                print(str(l), i)
        if line[0] == "cls" or line[0] == "clear":
            print("\033c")
        if line[0] == "save":
            if filename == "":
                print("No Filename Specified. Set it using setfilename command")
            else:
                with open(filename, "w") as f:
                    f.write("\n".join(buffer))
                savestatus = ''
        if line[0] == "setfilename":
            filename = line[1]
    except Exception as e:
        print(e)
