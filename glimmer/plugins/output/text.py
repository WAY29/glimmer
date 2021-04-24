from glimmer.api import PluginOutputBase, register_plugin, cprint, header


class Plugin(PluginOutputBase):
    def construct(self):
        self._handler = open("result.txt", "w+")

    def handle(self, poc, result, **kwargs):
        status = result.get('status', -1)
        sign = ""
        if status == 0:
            sign = "+"
        elif status == 1:
            sign = "-"
        elif status == -1:
            sign = "!"

        extra = result.get('extra', {})
        msg = '[cyan]%s[/cyan] %s <- %s (%s)' % (poc.name,
                                                 result.get("msg", ""), ",".join(result.get("hit_urls", [])), result.get("url"))
        if extra:
            msg += " extra: "
            msg += " ".join("%s:%s" % (k, v) for k, v in extra.items())
        if self.output_filter(status):
            self._handler.write("[Poc] %s %s\n" % (sign, msg))
            self._handler.flush()

    def destruct(self):
        self._handler.close()
        del self._handler

        cprint(header("Poc", "*", "Result save in ./result.txt"))


register_plugin(Plugin)
