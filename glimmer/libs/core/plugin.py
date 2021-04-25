from glimmer.libs.core.config import CONFIG, PLUGINS, AttribDict


class PluginBase():
    def construct(self):
        ...

    def destruct(self):
        ...
    ...


class PluginParserBase(PluginBase):
    protocols = [""]

    def protocol_check(self, module_path):
        return any(module_path.startswith(p) for p in self.protocols)

    def remove_protocol(self, module_path):
        for protocol in self.protocols:
            if module_path.startswith(protocol + "://"):
                return module_path[len(protocol)+3:]
        return module_path

    def get_protocol(self, module_path):
        for protocol in self.protocols:
            if module_path.startswith(protocol + "://"):
                return protocol
        return ""


class PluginOutputBase(PluginBase):

    def handle(self, poc, result, **kwargs):
        ...

    def output_filter(self, status):
        debug = CONFIG.option.get("debug", False)
        verbose = CONFIG.option.get("verbose", False)
        return (status == 0) or debug or verbose


CLASS_TO_NAME_DICT = {PluginOutputBase: "output", PluginParserBase: "parser"}


def register_plugin(plugin_class):
    plugin_name = plugin_class.__module__.split('.')[-1]
    plugin_type = "base"
    plugin_instance = plugin_class()
    for k, v in CLASS_TO_NAME_DICT.items():
        if isinstance(plugin_instance, k):
            plugin_type = v
            break
    if not hasattr(PLUGINS, plugin_type):
        PLUGINS[plugin_type] = AttribDict()
    PLUGINS.instances["%s/%s" % (plugin_type, plugin_name)] = plugin_instance
    PLUGINS[plugin_type][plugin_name] = plugin_instance
