from shlex import split as shlex
import argparse
import os.path
from os import environ
from os import name as osname

if osname == "nt":
    # windows version of readline
    import pyreadline
else:
    # linux version
    import readline
import configparser
from traceback import print_exc
import datetime
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter
from pygments.util import ClassNotFound

# plugins import
import plugins


def highlight_code(code, language):
    try:
        lexer = get_lexer_by_name(language, stripall=True)
        formatter = TerminalFormatter()
        return str(highlight(code, lexer, formatter))[:-1]
    except ClassNotFound:
        return code


def help(dictionary, key_to_help_with=None):
    print("-- HELP --")
    if key_to_help_with is None:
        # If no specific key is provided, print help for all keys
        for key, value in dictionary.items():
            print(f"{key}:\n {str(value[0])}\n {str(value[1])}")
    else:
        # If a specific key is provided, print help for that key
        if key_to_help_with in dictionary:
            print(
                f"{key_to_help_with}:\n {str(dictionary[key_to_help_with][0])}\n {str(dictionary[key_to_help_with][1])}"
            )
        else:
            print(f"No help available for '{key_to_help_with}'.")


defconf = environ["HOME"] + "/.config/safe.ini"

parser = argparse.ArgumentParser(
    prog="SAFE: Slow As F**k Editor",
    description="Edit files in a shell-like environment to make editing slower",
)

parser.add_argument(
    "filename",
    default="",
    nargs="?",
    help="Optional file name.",
)
parser.add_argument(
    "-s", "--script", help="Lets you run a script to edit files automatically."
)
parser.add_argument("-c", "--config", help="Config File to use.", default=defconf)
args = parser.parse_args()


config = configparser.ConfigParser()
config.read(args.config)
conf_nf = config["SHELL"].getboolean("NerdFontIcons")


def getreltime():
    ts = os.path.getmtime(filename)
    now = datetime.datetime.now()
    dt = datetime.datetime.fromtimestamp(ts)
    delta = now - dt
    final = ""
    if delta.days >= 365:
        years = delta.days // 365
        final += f"{years} year{'s' if years > 1 else ''} "
        delta -= datetime.timedelta(days=years * 365)

    if delta.days >= 30:
        months = delta.days // 30
        final += f"{months} month{'s' if months > 1 else ''} "
        delta -= datetime.timedelta(days=months * 30)

    if delta.days > 0:
        final += f"{delta.days} day{'s' if delta.days > 1 else ''} "

    if delta.seconds >= 3600:
        hours = delta.seconds // 3600
        final += f"{hours} hour{'s' if hours > 1 else ''} "
        delta -= datetime.timedelta(seconds=hours * 3600)

    if delta.seconds >= 60:
        minutes = delta.seconds // 60
        final += f"{minutes} minute{'s' if minutes > 1 else ''} "
        delta -= datetime.timedelta(seconds=minutes * 60)

    if delta.seconds > 0:
        final += f"{delta.seconds} second{'s' if delta.seconds > 1 else ''} "

    if final == "":
        final = "Just Now"

    return final


def getbytes(s):
    s = "\n".join(s)
    return len(s.encode("utf-8"))


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
var = {}
lang = ""


for name, value in environ.items():
    var[name] = value

readline.set_history_length(100)


def parsevars(line):
    all = list(var.keys())
    all.reverse()  # reverse() is used to make sure that i.e: $TERMINFO doesnt return the value of $TERM.
    for k in all:
        line = line.replace(f"${k}", var[k])

    return line


def run_cmd(line):
    global filename, debugmode, savestatus, var, lang
    line = parsevars(line)
    line = shlex(line)
    if len(line) < 1:
        return ""
    line[0] = line[0].lower()
    if line[0] == "edit":
        buffer[int(line[1]) - 1] = line[2]
        savestatus = "* "
    elif line[0] == "var":  # might add other variable types but idk what
        if line[1] == "normal":
            var[line[2]] = line[3]
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
        b = "\n".join(buffer)
        b = highlight_code(b, lang)
        for l, i in enumerate(b.split("\n")):
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
    elif line[0] == "setfiletype":
        lang = line[1]
    elif line[0] == "help":
        if len(line) > 1:
            s = line[1]
        else:
            s = None
        help(
            {
                "insert": [["index", "string"], "Inserts a string at a line index."],
                "edit": [["index", "string"], "Replaces a specific line by index."],
                "delete": [
                    ["pos1", "(optional) pos2"],
                    "Deletes a line or a range of lines from pos1 to pos2.",
                ],
                "cat": [["None"], "Prints out the current buffer."],
                "cls": [["None"], "Clears the screen."],
                "clear": [["None"], "Clears the screen."],
                "save": [["None"], "Saves the file with the current filename."],
                "setfilename": [
                    ["filename"],
                    "Sets the filename to be used with the save command.",
                ],
                "exit": [["None"], "Exits the program (wont save!!!)"],
                "debug": [
                    ["None"],
                    "Toggles debug mode (print full python tracebacks).",
                ],
                "info": [
                    ["None"],
                    "Shows some info about the current file if the file has a filename.",
                ],
                "setfiletype": [
                    ["filetype"],
                    "Sets the filetype to be used with the 'cat' command.",
                ],
            },
            s,
        )
    elif line[0] == "setfilename":
        filename = line[1]
    elif line[0] == "debug":
        debugmode = not debugmode
    elif line[0] == "exit":
        if savestatus == "* ":
            if (
                input(
                    "WARNING! You have unsaved changes. Are you sure you want to quit? (y/N)"
                ).lower()
                == "y"
            ):
                exit()
        else:
            exit()
    elif line[0] == "info":
        if not filename == "" and os.path.exists(filename):
            print(
                f"Last Modified: {getreltime()}\nSize In Bytes: {os.path.getsize(filename)}"
            )
    else:
        print("Command not recognized!")


if not args.script:
    while 1:
        try:
            line = input(
                f"{getbytes(buffer)}{savestatus}{filename if filename != '' else 'unnamed'} $ "
            )
            readline.add_history(line)
            line = line.split("&&")
            for l in line:
                run_cmd(l)
        except KeyboardInterrupt as e:
            print('\nCtrl+C pressed, please use "exit" command to quit.')
        except Exception as e:
            if debugmode:
                print_exc()
            else:
                print(e)

else:
    script = open(args.script, "r").read()
    for i in str(script).split("\n"):
        i = i.split("&&")
        for l in i:
            run_cmd(l)
    run_cmd("save")
    run_cmd("exit")
