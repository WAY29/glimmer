from api import PluginParserBase, register_plugin, requests
from utils import is_valid_url


class Plugin(PluginParserBase):
    protocols = ["http", "https"]

    def rule_check(self, module_path):
        return is_valid_url(module_path) and self.protocol_check(module_path)

    def get_data(self, module_path):
        try:
            res = requests.get(module_path)
            return res.text
        except Exception:
            return ""


register_plugin(Plugin)
