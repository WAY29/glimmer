from rich.console import Console

CONSOLE = Console()
cprint = CONSOLE.print


def header(typ: str = "Base", sign: str = "", msg: str = "") -> str:
    if sign == "+":
        sign = " [green][+][/green]"
    elif sign == "-":
        sign = " [red][-][/red]"
    elif sign == "!":
        sign = " [yellow][+][/yellow]"
    elif sign == "*":
        sign = " [cyan][*][/cyan]"
    else:
        sign = ""
    return "[cyan][%s][/cyan]%s %s" % (typ, sign, msg)


__all__ = ["CONSOLE", "cprint", "header"]
