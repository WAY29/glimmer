from rich.console import Console

CONSOLE = Console()
cprint = CONSOLE.print
print_traceback = CONSOLE.print_exception


def header(typ: str = "Base", sign: str = "", msg: str = "") -> str:
    if sign == "+":
        sign = "[green][+][/]"
    elif sign == "-":
        sign = "[red][-][/]"
    elif sign == "!":
        sign = "[yellow][!][/]"
    elif sign == "*":
        sign = "[cyan][*][/]"
    else:
        sign = "[magenta][?][/]"
    if typ:
        typ = "[cyan]%s[/]" % typ.strip()
    s = "%s %-40s %s" % (sign, msg.strip(), typ)
    return s


__all__ = ["CONSOLE", "cprint", "header", "print_traceback"]
