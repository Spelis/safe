import argparse
import os.path
from difflib import get_close_matches
from os import environ, listdir
from os import name as osname
from os import system
from random import randint
from shlex import split as shlex

if osname == "nt":
    import pyreadline  # windows version of readline
else:
    from readline import *  # linux version

import importlib.util
import sys
from string import Template
from traceback import print_exc

import func

scriptdir = os.path.dirname(__file__)
for i in os.listdir(f"{scriptdir}/defmod/"):
    if i == "__pycache__":
        continue  # dont try to import pycache
    spec = importlib.util.spec_from_file_location(
        i.split(".")[0], f"{scriptdir}/defmod/{i}"
    )
    m = importlib.util.module_from_spec(spec)
    sys.modules[i.split(".")[0]] = m
    spec.loader.exec_module(m)
    globals().update(m.__dict__)  # import * from ...
    func.modules.append(m)

ap = argparse.ArgumentParser("SAFE: Slow as f**k editor")

ap.add_argument(
    "filename",
    default="",
    nargs="*",
    help="Optional file name.",
)
ap.add_argument("-s", "--script")

args = ap.parse_args()
del ap

for i in args.filename:
    func.openfile(i)
if len(args.filename) == 0:
    func.buffers["New File"] = func.FileObject("New File")
    func.buffers["New File"].unnamed = True
    func.curbuf = "New File"

if osname != "nt":
    set_history_length(100)
    comp = func.InputCompleter()
    set_completer(comp.completer)
    parse_and_bind("tab: complete")

import config  # run config file here


def run_cmd(line):
    raw = line
    arg = shlex(line, True)  # comments cause why not
    command = arg.pop(0)
    try:
        call: func.FnMeta = func.commands[command]
    except KeyError as e:
        try:
            print(
                f"command '{command}' doesnt exist. did you mean {get_close_matches(command,list(func.commands.keys()),1)[0]}?"
            )
        except:
            print(f"command '{command}' doesnt exist")
        return
    positionals = [item for item in arg if "=" not in item]
    for i in range(len(positionals)):
        positionals[i] = list(call.annotations.values())[i](positionals[i])
    keywords = {pair.split("=")[0]: pair.split("=")[1] for pair in arg if "=" in pair}
    for k, v in keywords:
        keywords[k] = call.annotations[k](v)
    if func.debug:
        print(call.meta())
    call(*positionals, **keywords)


if not args.script:
    while 1:
        try:
            promptvars = {  # redefine every time the prompt reappears.
                "bytes": func.getbytes(func.buffer().buffer),
                "filename": func.buffer().filename,
                "savestatus": "" if func.buffer().saved else "* ",
                "lastsaved": func.getreltime(func.buffer().filename)
            }
            func.extendpromptvars(promptvars)  # load promptvars from other plugins
            line = input(
                Template(func.prompt).safe_substitute(promptvars)
            )  # use a template here
            if not line:  # line is empty
                continue
            if line.startswith("#"):
                continue  # is comment
            if osname != "nt":
                add_history(line)
            run_cmd(line)
        except KeyboardInterrupt:
            print("please use the 'exit' command to quit.")
        except Exception as e:
            print_exc()
else:
    debug = True  # debug enabled by default for scripts
    for i in args.filename:
        try:
            with open(i) as f:
                script = f.read()
                run_cmd(f"newfile {i}")
                for i in str(script).split("\n"):
                    i = i.split(";")
                    for l in i:
                        run_cmd(l)
                run_cmd("save")
                run_cmd("close")
        except:
            continue
