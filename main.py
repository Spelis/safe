from shlex import split as shlex
import argparse
import os.path
from os import environ, system, listdir
from os import name as osname
from random import randint
from subprocess import check_output

if osname == "nt":
    # windows version of readline
    import pyreadline
else:
    # linux version
    from readline import *
import configparser
from traceback import print_exc
import datetime
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter
from pygments.util import ClassNotFound
import re


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


defconf = os.path.expanduser("~/.config/safe.ini")

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

aliases = {}


config = configparser.ConfigParser()
config.read(args.config)
conf_nf = config.getboolean("SHELL", "NerdFontIcons", fallback=False)
conf_cc = config.getboolean("SHELL", "CtrlCQuit", fallback=False)
conf_cp = config.getboolean("SHELL", "ColorPrompt", fallback=False)
conf_cool = config.getboolean("SHELL", "CoolPrompt", fallback=False)
try:
    for k, v in config.items("ALIAS"):
        aliases[k] = v
except:
    pass


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
    # Join the input string with newline characters
    s = "\n".join(s)
    # Encode the string to bytes and get the length
    size_in_bytes = len(s.encode("utf-8"))

    # Convert to KB, MB, GB
    size_in_kb = size_in_bytes / 1024
    size_in_mb = size_in_kb / 1024
    size_in_gb = size_in_mb / 1024

    if size_in_gb > 1:
        return str(round(size_in_gb, 2)) + " GB"
    elif size_in_mb > 1:
        return str(round(size_in_mb, 2)) + " MB"
    elif size_in_kb > 1:
        return str(round(size_in_kb, 2)) + " KB"
    else:
        return str(round(size_in_bytes, 2)) + " Bytes"


def listinsert(list, ins_index, obj):
    llen = len(list)
    if ins_index > llen:
        for i in range(llen, ins_index - 1):
            list.insert(i, "")
        list.insert(ins_index - 1, obj)
    else:
        list.insert(ins_index, obj)
    return list

filename = ""

def openfile(fn='',new=False):
    global filename,buffer
    filename = fn
    if fn == "":
        buffer = [""]
    elif new == True:
        buffer = [""]
    elif not os.path.exists(fn):
        buffer = [""]
    else:
        with open(fn, "r") as f:
            buffer = str(f.read()).split("\n")
            
openfile(args.filename)

savestatus = " "
debugmode = False
var = {}
lang = ""


for name, value in environ.items():
    var[name] = value

if osname != "nt":
    set_history_length(100)


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
    line[0] = replace_aliases(line[0], aliases)
    line[0] = line[0].lower()
    if line[0] == "edit":
        buffer[int(line[1]) - 1] = " ".join(line[2:])
        savestatus = "* "
    elif line[0] == "var":  # might add other variable types but idk what
        if line[1] == "normal":
            var[line[2]] = line[3]
        if line[1] == "cmd":
            var[line[2]] = check_output(line[3])
    elif line[0] == "insert":
        listinsert(buffer, int(line[1]), " ".join(line[2:]))
        savestatus = "* "
    elif line[0] == "delete":
        if len(line) > 2:
            for i in range(int(line[2])):
                buffer.pop(int(line[1]))
        else:
            buffer.pop(int(line[1]) - 1)
        savestatus = "* "
    elif line[0] == "cat":
        if len(line) > 1:
            ln0 = int(line[1]) - 1
        else:
            ln0 = 0
        if len(line) > 2:
            ln1 = int(line[2])
        elif len(line) > 1:
            ln1 = int(line[1])
        else:
            ln1 = len(buffer)
        b = "\n".join(buffer[ln0:ln1])
        b = highlight_code(b, lang)
        for l, i in enumerate(b.split("\n")):
            print(str(l + ln0 + 1), i)
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
                "setfiletype": [
                    ["filetype"],
                    "Sets the filetype for syntax highlighting",
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
                "exec": [["Command"], "Executes a shell command"],
                "new": [["Filename (Optional)"],"Creates a new file"],
                "open": [["Filename"],"Opens a file"],
                "ls": [["Path (Optional)"],"Lists a directory (default is current directory"]
            },
            s,
        )
    elif line[0] == "exec":
        system(" ".join(line[1:]))
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
    elif line[0] == "new":
        if len(line) > 1:
            nm = line[1]
        else:
            nm = ''
        if savestatus == "* ":
            if (
                input(
                    "WARNING! You have unsaved changes. Are you sure you want to create a new file? (y/N)"
                ).lower()
                == "y"
            ):
                openfile(nm,True)
        else:
            openfile(nm,True)
    elif line[0] == "open":
        if savestatus == "* ":
            if (
                input(
                    "WARNING! You have unsaved changes. Are you sure you want to open this file? (y/N)"
                ).lower()
                == "y"
            ):
                openfile(line[1])
        else:
            openfile(line[1])
    elif line[0] == "ls":
        if len(line) > 1:
            path = line[1]
        else:
            path = None
        for i, v in enumerate(listdir(path)):
            fp = os.path.join(path if path is not None else '', v)
            if i % 6 == 5:
                print('')
                print(('\x1b[32m' if os.path.isdir(fp) else '') + v + ("/" if os.path.isdir(fp) else "") + '\x1b[0m ', end='')
            else:
                print(('\x1b[32m' if os.path.isdir(fp) else '') + v + ("/" if os.path.isdir(fp) else "") + '\x1b[0m ', end='')
        print('')
    elif line[0] == "info":
        if not filename == "" and os.path.exists(filename):
            print(f"Last Modified: {getreltime()}\nSize: {getbytes(buffer)}")
        else:
            print(f"Size: {getbytes(buffer)}")
    else:
        print(f"Command '{line[0]}' not recognized!")


back1 = randint(1, 12)
back2 = back1 + 3


def color(type, id, text=""):
    if conf_cp:
        if type == 0:
            return "\x1b[0m"
        else:
            return f'\x1b[{type if conf_cool else "3"}8;5;{id}m{text if conf_cool and conf_cp else ""}'
    else:
        return ""


def replace_aliases(line, aliases):
    # Sort aliases by length in descending order to handle substrings correctly
    sorted_aliases = sorted(
        aliases.items(), key=lambda item: len(item[0]), reverse=True
    )

    for alias, command in sorted_aliases:
        # Use regex to replace the alias with the command, considering word boundaries
        # This ensures that only whole words are replaced and not substrings of other words

        line = re.sub(r"\b" + re.escape(alias) + r"\b", command, line)

    return line


# plugins import
import plugins

if not args.script:
    while 1:
        try:
            line = input(
                f"{color(3,back1,'')}{color(3,0)+color(4,back1)}{'󰦨 ' if conf_nf else ''}{getbytes(buffer)}{color(3,back1)+color(4,back2,'')}{color(3,0)+color(4,back2)}{savestatus.replace('*','•')}{' ' if conf_nf else ''}{filename if filename != '' else 'unnamed'} {color(0,0)+color(3,back2,'')}{'' if conf_cool else '$'}{color(0,0)} "
            )
            if osname != "nt":
                add_history(line)
            line = line.split("&&")
            for l in line:
                run_cmd(l)
        except KeyboardInterrupt as e:
            if not conf_cc:
                print('\nCtrl+C pressed, please use "exit" command to quit.')
            else:
                break
        except Exception as e:
            if debugmode:
                print_exc()
            else:
                print(e)

else:
    try:
        script = open(args.script, "r").read()
        debugmode = True
        for i in str(script).split("\n"):
            i = i.split("&&")
            for l in i:
                run_cmd(l)
        run_cmd("save")
        run_cmd("exit")
    except Exception as e:
        if debugmode:
            print_exc()
        else:
            print(e)
