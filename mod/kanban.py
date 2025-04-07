import pickle

import func

kanbans = func.AttrDict({"boards": {}, "current": ""})


def promptvars():
    global kanbans
    vars = {"curkan": kanbans.current}
    return vars


def kanban():
    if not kanbans.current or kanbans.current not in kanbans.boards:
        raise ValueError("No current Kanban board selected")
    return kanbans.boards[kanbans.current]


class KanbanComp(str):
    """(str) Kanban Board"""

    def complete(text):
        return [
            f'"{board}"' if " " in board else board
            for board in kanbans.boards.keys()
            if board.startswith(text)
        ]


class Column(str):
    """(str) Kanban board Column"""

    def complete(text):
        try:
            current_board = kanban()
        except ValueError:
            return []
        return [
            f'"{col}"' if " " in col else col
            for col in current_board.columns.keys()
            if col.startswith(text)
        ]


class KanbanBoard:
    def __init__(self, filename):
        self.filename = filename
        self.columns = {}


class KanbanColumn:
    def __init__(self):
        self.cards = {}


@func.localcommand("new")
def newboard(name: str):
    """Create a Kanban board"""
    if name in kanbans.boards:
        print(f"Board '{name}' already exists")
        return
    kanbans.boards[name] = KanbanBoard(name)
    kanbans.current = name


@func.localcommand()
def close():
    """Delete the current Kanban board"""
    if kanbans.current in kanbans.boards:
        del kanbans.boards[kanbans.current]
        if kanbans.boards:
            kanbans.current = next(iter(kanbans.boards.keys()))
        else:
            kanbans.current = ""
    else:
        print("No board to close")


@func.localcommand("list")
def listboards():
    """List all Kanban boards"""
    for name, board in kanbans.boards.items():
        print(f"{name}: {list(board.columns.keys())}")


@func.localcommand()
def info():
    """Info on current Kanban"""
    try:
        board = kanban()
        print(f"{board.filename}:")
        for col_name, col in board.columns.items():
            print(f"  {col_name}:")
            for card_name, card in col.cards.items():
                print(f"    {card_name}: {card}")
    except ValueError as e:
        print(e)


@func.localcommand()
def switchto(board: KanbanComp):
    """Switch board"""
    if board in kanbans.boards:
        kanbans.current = board
    else:
        print(f"Board '{board}' does not exist")


@func.localcommand()
def newcolumn(name: str):
    """Create a new column in the current Kanban board"""
    try:
        k = kanban()
        if name in k.columns:
            print(f"Column '{name}' already exists")
            return
        k.columns[name] = KanbanColumn()
    except ValueError as e:
        print(e)


@func.localcommand()
def newcard(column: Column, title: str, value: str = "..."):
    """Create a new card in a column"""
    try:
        k = kanban()
        if column not in k.columns:
            print(f"Column '{column}' does not exist")
            return
        if title in k.columns[column].cards:
            print(f"Card '{title}' already exists in column '{column}'")
            return
        k.columns[column].cards[title] = value
    except ValueError as e:
        print(e)


# New commands for board management
@func.localcommand()
def movecard(card_title: str, from_column: Column, to_column: Column):
    """Move a card between columns"""
    kb = kanban()
    if from_column not in kb.columns or to_column not in kb.columns:
        print("One or both columns don't exist")
        return
    if card_title not in kb.columns[from_column].cards:
        print(f"Card '{card_title}' not found in {from_column}")
        return

    card = kb.columns[from_column].cards.pop(card_title)
    kb.columns[to_column].cards[card_title] = card


@func.localcommand()
def deletecolumn(column: Column):
    """Delete a column (and its cards)"""
    kb = kanban()
    if column not in kb.columns:
        print(f"Column '{column}' doesn't exist")
        return
    del kb.columns[column]


@func.localcommand()
def deletecard(column: Column, card_title: str):
    """Delete a card from a column"""
    kb = kanban()
    if column not in kb.columns:
        print(f"Column '{column}' doesn't exist")
        return
    if card_title not in kb.columns[column].cards:
        print(f"Card '{card_title}' not found")
        return
    del kb.columns[column].cards[card_title]


@func.localcommand()
def renameboard(new_name: str):
    """Rename current board"""
    if new_name in kanbans.boards:
        print(f"Board '{new_name}' already exists")
        return
    current = kanbans.current
    kanbans.boards[new_name] = kanbans.boards.pop(current)
    kanbans.current = new_name
    kanbans.boards[new_name].filename = new_name


@func.localcommand()
def renamecolumn(old_name: Column, new_name: str):
    """Rename a column in current board"""
    kb = kanban()
    if old_name not in kb.columns:
        print(f"Column '{old_name}' doesn't exist")
        return
    if new_name in kb.columns:
        print(f"Column '{new_name}' already exists")
        return
    kb.columns[new_name] = kb.columns.pop(old_name)


@func.localcommand()
def renamecard(column: Column, old_title: str, new_title: str):
    """Rename a card in a column"""
    kb = kanban()
    if column not in kb.columns:
        print(f"Column '{column}' doesn't exist")
        return
    cards = kb.columns[column].cards
    if old_title not in cards:
        print(f"Card '{old_title}' not found")
        return
    if new_title in cards:
        print(f"Card '{new_title}' already exists")
        return
    cards[new_title] = cards.pop(old_title)


@func.localcommand("save")
def saveboard(filename: str = "kanbans.pkl"):
    """Save all boards to file"""
    try:
        with open(filename, "wb") as f:
            pickle.dump(kanbans, f)
        print(f"Saved to {filename}")
    except Exception as e:
        print(f"Error saving: {e}")


@func.localcommand("load")
def loadboard(filename: str = "kanbans.pkl"):
    """Load boards from file"""
    global kanbans
    try:
        with open(filename, "rb") as f:
            loaded = pickle.load(f).__dict__
            # Validate loaded data structure
            if isinstance(loaded, dict) and "boards" in loaded and "current" in loaded:
                kanbans = func.AttrDict(loaded)
                print(f"Loaded from {filename}")
            else:
                print("Invalid kanban data file")
    except FileNotFoundError:
        print("No saved boards found")
    except Exception as e:
        print(f"Error loading: {e}")
