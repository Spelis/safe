import random

import func,os
from pathlib import Path


class LineNumber(int):
    """(int) Line Number of a Buffer"""

    def complete(text):
        return [random.randint(1, len(func.buffer().buffer))]  # i did a funny :)


class File(str):
    """(str) Any file anywhere"""

    def complete(text):
        """Generate directory-aware path completions"""
        # Split into base directory and partial filename
        base_dir, partial = os.path.split(text)
        base_dir = base_dir or '.'  # Use current directory if empty
        
        try:
            # List directory contents
            full_dir = Path(base_dir).resolve()
            matches = []
            
            for item in os.listdir(full_dir):
                item_path = full_dir / item
                # Match items starting with partial
                if item.startswith(partial):
                    # Build the full matched path
                    matched_path = os.path.join(base_dir, item)
                    # Add slash for directories
                    if item_path.is_dir():
                        matched_path += os.sep
                    matches.append(matched_path)
            
            return matches
            
        except (FileNotFoundError, NotADirectoryError):
            return []


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
