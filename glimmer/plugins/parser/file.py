from api import PluginParserBase, register_plugin
from utils import is_valid_pathname


class Plugin(PluginParserBase):
    protocols = ["file"]

    def rule_check(self, module_path):
        return is_valid_pathname(module_path) and self.protocol_check(module_path)

    def get_data(self, module_path):
        module_path = self.remove_protocol(module_path)
        with open(module_path, "r") as f:
            return f.read()
        return ""


register_plugin(Plugin)
