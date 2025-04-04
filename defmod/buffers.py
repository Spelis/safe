import os
import sys
from copy import copy

import completiontypes as ct
import func


@func.command
def openfile(filename: ct.File):
    """Open a file in current tab"""
    func.openfile(filename)


@func.command
def newfile(filename: str):
    """Create a new tab and file"""
    func.openfile(filename, True)


@func.command
def savefile(filename: str = None):
    """Save the current file, optionally provide a filename to \"save as\" """
    buf = func.buffer()
    with open(buf.filename, "w") as f:
        f.write("\n".join(buf.buffer))
    print("Saved!")


@func.command
def switchbuf(filename: ct.Buffer):
    """Switch buffers"""
    if filename in func.buffers.keys():
        func.curbuf = filename
    else:
        print("Buffer doesn't exist.")
        print(f"Buffers: {list(func.buffers.keys())}")


@func.command
def listbuf():
    """List all buffers"""
    for k, v in func.buffers.items():
        print(f"{k}: {len(v.buffer)} lines")


@func.command
def renamebuf(filename: ct.File):
    """Rename the current buffer"""
    buf: func.FileObject = copy(func.buffer())
    buf.filename = filename
    buf.saved = False
    buf.unnamed = False
    del func.buffers[func.curbuf]
    func.buffers[filename] = buf
    func.curbuf = filename


@func.command
def close():
    """Close the current buffer"""
    del func.buffers[func.curbuf]
    if func.buffers == {}:
        exit()
    else:
        func.curbuf = list(func.buffers.keys())[0]  # first buffer in the buffer list


@func.command
def exit():
    """Exit all buffers and the program without saving"""
    sys.exit(0)


@func.command
def cat(line: ct.LineNumber = 1, line2: ct.LineNumber = 0):
    """Print out file contents, optionally in a range or just a single line"""
    buf: func.FileObject = func.buffer()
    ln0 = line - 1
    ln1 = len(buf.buffer) if line2 == 0 else line2
    b = "\n".join(buf.buffer[ln0:ln1])
    b = func.highlight_code(b, buf.filename)
    b = b.split("\n")
    if len(buf.buffer) > len(b):
        for i in range(len(b), len(buf.buffer)):
            b.insert(i, "")
    for l, i in enumerate(b):
        print(str(l + ln0 + 1) + " " * (len(str(len(buf.buffer))) - 1), i)


@func.command
def edit(line: ct.LineNumber, value: str):
    """Edit a line"""
    buf = func.buffer()
    buf.buffer[line - 1] = value
    buf.saved = False


@func.command
def insert(line: ct.LineNumber, value: str = ""):
    """Insert text at line"""
    buf = func.buffer()
    if line > len(buf.buffer):
        for i in range(len(buf.buffer), line - 1):
            buf.buffer.insert(i, "")
    buf.buffer.insert(line, value)
    buf.saved = False


@func.command
def delete(line: ct.LineNumber, times: ct.LineNumber = 1):
    """Delete lines"""
    for _ in range(times):
        func.buffer().buffer.pop(line - 1)
