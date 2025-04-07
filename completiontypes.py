import random

import func


class LineNumber(int):
    """(int) Line Number of a Buffer"""

    def complete(text):
        return [random.randint(1, len(func.buffer().buffer))]  # i did a funny :)


class File(str):
    """(str) Any file anywhere"""

    def complete(text):
        return [
            str(func.Path(file).relative_to(func.os.getcwd()))
            for file in func.r_listdir(func.os.getcwd())
            if str(func.Path(file).relative_to(func.os.getcwd())).startswith(text)
        ]


class Buffer(str):
    """(str) Any opened file (buffer)"""

    def complete(text):
        return [
            (f'"{buf}"' if " " in buf else f"{buf}")
            for buf in list(func.buffers.keys())
            if buf.startswith(text)
        ]


class Command(str):
    """(str) Any defined command"""

    def complete(text):
        return [
            (f'"{cmd}"' if " " in cmd else f"{cmd}")
            for cmd in list(func.commands.keys())
            if cmd.startswith(text)
        ]


class Code(str):
    """(str) Code, pretty self explanatory"""

    def complete(text):
        return [f'"{text}"']

    # might be used for LSP support later on if i can be arsed to implement it
