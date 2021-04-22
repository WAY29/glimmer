from glimmer.utils import cprint
from glimmer.libs.core.enums import POC_TYPE


class PocBase():
    """
        No description.
    """
    vulid = "-1"
    type = POC_TYPE.UNKNOWN
    version = "1.0"
    authors = ["Unknown"]
    references = [""]
    name = ""
    appName = ""
    appVersion = ""

    def show_info(self):
        vuln_app_info = ""
        if self.appName:
            vuln_app_info = "[red]Vulnable App[/]: %s" % self.appName
            if self.appVersion:
                vuln_app_info += " (%s)" % self.appVersion
        cprint("""
[%s] [cyan]%s[/] - %s (%s)
[yellow]Authors[/]: %s
[magenta]References[/]: %s
%s
[blue]Description[/]:
  %s
""" %
               (self.vulid, self.name, self.version, self.type, ",".join(self.authors), "  ".join(
                   self.references), vuln_app_info, self.__doc__.strip())
               )
