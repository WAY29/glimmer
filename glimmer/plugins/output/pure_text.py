from glimmer.api import PluginOutputBase, register_plugin, cprint, header


class Plugin(PluginOutputBase):
    def construct(self):
        self._handler = open("pure_result.txt", "w+")

    def handle(self, poc, result, **kwargs):
        status = result.get('status', -1)
        write_urls = "\n".join(result.get("hit_urls", []))
        if write_urls:
            write_urls += "\n"

        if not status:
            self._handler.write(write_urls)
            self._handler.flush()

    def destruct(self):
        self._handler.close()
        del self._handler

        cprint(header("Poc", "*", "Result save in ./pure_result.txt"))


register_plugin(Plugin)
