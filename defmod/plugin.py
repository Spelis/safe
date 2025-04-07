import importlib
import os
import sys
from difflib import get_close_matches
from pathlib import Path

import completiontypes as ct
import func


@func.globalcommand()
def help(command: ct.Command = ""):
    """Help command. shows this message"""
    if not command:
        for i in func.commands.values():
            print(
                "{} - {}:{}\n  {}{}  {}".format(
                    i.name,
                    i.file,
                    i.line,
                    i.help,
                    "\n" if len(i.args) > 0 else "",
                    ", ".join(i.args),
                )
            )
    else:
        try:
            i: func.FnMeta = func.commands[command]
            print(
                "{} - {}:{}\n  {}{}  {}".format(
                    i.name,
                    i.file,
                    i.line,
                    i.help,
                    "\n" if len(i.args) > 0 else "",
                    ", ".join(i.args),
                )
            )
        except KeyError:
            try:
                print(
                    f"command '{command}' doesnt exist. did you mean {get_close_matches(command,list(func.commands.keys()),1)[0]}?"
                )
            except:
                print(f"command '{command}' doesnt exist")


scriptpath = Path(*Path(__file__).parts[:-2])


class Plugin(str):
    """(str) Plugins (inside ./mod/ folder)"""

    def complete(text):
        return [
            str(".".join(file.split(".")[:-1]))
            for file in os.listdir(str(Path(scriptpath) / "mod"))
            if file.startswith(text) and file.endswith(".py")
        ]


@func.globalcommand()
def loadplugin(filename: Plugin):
    """Load a module"""
    spec = importlib.util.spec_from_file_location(
        filename, f"{scriptpath}/mod/{filename}.py"
    )
    m = importlib.util.module_from_spec(spec)
    sys.modules[filename] = m
    spec.loader.exec_module(m)
    globals().update({f"{filename}.{k}": v for k, v in m.__dict__.items()})
    func.modules.append(m)
