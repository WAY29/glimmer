from rich.console import Console

CONSOLE = Console()
cprint = CONSOLE.print
print_traceback = CONSOLE.print_exception


def header(typ: str = "Base", sign: str = "", msg: str = "") -> str:
    if sign == "+":
        sign = " [green][+][/green]"
    elif sign == "-":
        sign = " [red][-][/red]"
    elif sign == "!":
        sign = " [yellow][!][/yellow]"
    elif sign == "*":
        sign = " [cyan][*][/cyan]"
    else:
        sign = ""
    if typ:
        typ = "[cyan][%s][/cyan]" % typ
    else:
        sign = sign.strip()
    return "%s%s %s" % (typ, sign, msg)


__all__ = ["CONSOLE", "cprint", "header", "print_traceback"]
