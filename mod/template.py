import func


def promptvars():
    return {"template": 0}


class CompletionTemplate(str):
    """(str) Completion template"""

    def complete(text):
        return [
            f'"{comp}"' if " " in comp else comp
            for comp in ["one", "two", "three"]
            if comp.startswith(text)
        ]


@func.globalcomman()
def templatecommand(thing: CompletionTemplate):
    """Command with no prefix that uses a custom completer (one,two or three)"""
    print(f"template: {thing}")


@func.localcommand()
def printtext(text: str):
    """Command with prefix (template) that prints the text you supply it with"""
    print(text)
