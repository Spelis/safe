import datetime
import difflib
import functools
import inspect
import os
import readline
from ast import literal_eval as literal_eval
from pathlib import Path
from shlex import split as shlex
from traceback import print_exc
from typing import Any, Dict, Optional

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound

import completiontypes as ct

global commands, buffers, curbuf
commands = {}
buffers = {}
curbuf = ""


class FileObject:
    def __init__(self, fn):
        self.filename = fn
        self.buffer = []
        self.saved = True
        self.language = ""
        self.unnamed = False


errorbuffer = FileObject("NullFile")


def buffer() -> FileObject:
    """Return the active buffer"""
    try:
        return buffers[curbuf]
    except:
        return errorbuffer


class FnMeta:
    def __init__(self, func) -> None:
        self.func = func
        self.name = func.__name__
        self.help = getattr(func, "__doc__", "No help provided.")
        self.line = inspect.getsourcelines(func)[-1]
        self.file = Path(*Path(inspect.getsourcefile(func)).parts[-2:])

        sig = inspect.signature(func)
        self.args = [param.name for param in sig.parameters.values()]
        self.annotations = {
            param.name: param.annotation
            for param in sig.parameters.values()
            if param.annotation != param.empty
        }

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


def command(func):
    meta = FnMeta(func)
    commands[meta.name] = meta

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def r_listdir(dir):
    """Recurive Directory Listing"""
    o = []
    for i in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, i)):
            o.extend(reversed(r_listdir(os.path.join(dir, i))))
        else:
            o.append(os.path.join(dir, i))
    return sorted(o, key=len, reverse=True)


def inputcompleter(text: str, state: int):
    matches = []
    full = readline.get_line_buffer()
    try:
        parsed = shlex(full)
    except:
        parsed = shlex(full + '"')
    arg = full.count(" ") - 1
    if len(parsed) == 0:
        parsed.append("")
    cmd = parsed[0]
    parsed = parsed[-1]
    if state == 0:
        if arg == -1:
            matches = [cmd for cmd in list(commands.keys()) if cmd.startswith(text)]
            # matches.extend(difflib.get_close_matches(text,list(commands.keys()),n=len(commands.keys())))
        if cmd in commands.keys():
            if arg >= 0 and arg <= len(commands[cmd].args):
                atype = commands[cmd].annotations[commands[cmd].args[arg]]
                if atype == ct.Command:
                    matches = [
                        (f'"{cmd}"' if " " in cmd else f"{cmd}")
                        for cmd in list(commands.keys())
                        if cmd.startswith(text)
                    ]
                elif atype == ct.Buffer:
                    matches = [
                        (f'"{buf}"' if " " in buf else f"{buf}")
                        for buf in list(buffers.keys())
                        if buf.startswith(text)
                    ]
                elif atype == ct.File:
                    matches = list(
                        str(Path(file).relative_to(os.getcwd()))
                        for file in r_listdir(os.getcwd())
                        if str(Path(file).relative_to(os.getcwd())).startswith(text)
                    )
                elif atype == ct.Code:
                    matches = [f'"{text}"']

    matches = list(set(matches))  # remove duplicates
    try:
        return matches[state]
    except Exception as e:
        # print_exc()
        return None


def getreltime(filename):
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


def openfile(fn="", new=False):
    global buffer, curbuf
    curbuf = fn
    if not fn:
        fn = f"New File {len(buffers.values())}"
    buf = buffer()
    if fn == "" or new == True or not os.path.exists(fn):
        buf = FileObject(fn)
        buf.unnamed = True
    else:
        with open(fn, "r") as f:
            buf = FileObject(fn)
            buf.buffer = str(f.read()).split("\n")
    buffers[fn] = buf


def autotype(obj) -> Any:
    try:
        return literal_eval(obj)
    except:
        return obj


def highlight_code(code, filename):
    try:
        lexer = get_lexer_for_filename(filename, stripall=True)
        formatter = TerminalFormatter()
        return str(highlight(code, lexer, formatter))[:-1]
    except ClassNotFound:
        return code


class ConfigClass:
    def exec(self, command, *args, **kwargs):
        commands[command](*args, **kwargs)


config = ConfigClass()


prompt = "$savestatus$bytes $filename: "
