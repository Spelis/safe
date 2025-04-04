class LineNumber(int):
    """(int) Line Number of a Buffer"""


class File(str):
    """(str) Any file anywhere"""


class Buffer(str):
    """(str) Any opened file (buffer)"""


class Command(str):
    """(str) Any defined command"""


class Code(str):
    """(str) Code, pretty self explanatory"""

    # currently unused, might be used for LSP support later on if i can be arsed to implement it
