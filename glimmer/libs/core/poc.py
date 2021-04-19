from utils import cprint


class PocBase():
    """
        No description.
    """
    vulid = "-1"
    version = "1.0"
    authors = ["Unknown"]
    references = [""]
    name = ""
    appName = ""
    appVersion = ""

    def show_info(self):
        cprint("""
%s [cyan]%s[/] (%s)
Authors: [yellow]%s[/yellow]
References: [green]%s[/green]
Vulnable App: [red]%s[/red] (%s)
Description:
  %s
""" %
               (self.vulid, self.name, self.version, ",".join(self.authors), "  ".join(self.references), self.appName, self.appVersion, self.__doc__.strip())
               )
