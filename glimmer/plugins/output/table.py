from glimmer.api import PluginOutputBase, register_plugin, cprint, rich


class Plugin(PluginOutputBase):
    def construct(self):
        table = rich.table.Table(title="Result")
        table.add_column("poc", style="magenta", justify="center")
        table.add_column("status", justify="center")
        table.add_column("message", justify="center")
        table.add_column("url", style="cyan", justify="center")
        self._table = table

    def handle(self, poc, result, **kwargs):
        table = self._table
        status = result.get('status', -1)
        status_msg = ""
        if status == 0:
            status_msg = "[green]success[/]"
        elif status == 1:
            status_msg = "[red]failed[/]"
        elif status == -1:
            status_msg = "[yellow]error[/]"
        table.add_row(poc.name, status_msg, result.get(
            "msg", ""), result.get("url"))

    def destruct(self):
        if self._table.row_count > 0:
            cprint(self._table)


register_plugin(Plugin)
