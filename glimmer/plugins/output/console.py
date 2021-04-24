from glimmer.api import PluginOutputBase, register_plugin, cprint, header


class Plugin(PluginOutputBase):
    def handle(self, poc, result, **kwargs):
        """
        data example:
        {
            'url': 'http://baidu.com',
            'status': 0,
            'msg': 'demo2 poc success',
            'hit_urls': ['http://baidu.com', ],
            'extra': {}
        }
        """
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
            cprint(header("Poc", sign, msg))


register_plugin(Plugin)
