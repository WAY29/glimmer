from glimmer.api import PluginParserBase, register_plugin, requests, is_valid_url
from urllib import parse


class Plugin(PluginParserBase):
    protocols = ["repo"]

    def get_raw_url(self, module_path):
        module_path = module_path if module_path.endswith(".py") else module_path + ".py"
        return parse.urljoin("https://gitee.com/guuest/glimmer_pocs/raw/master/", self.remove_protocol(module_path))

    def rule_check(self, module_path):
        return self.protocol_check(module_path) and is_valid_url(self.get_raw_url(module_path))

    def get_data(self, module_path):
        try:
            res = requests.get(self.get_raw_url(module_path), verify=False)
            return (res.text, )
        except Exception:
            return ()


register_plugin(Plugin)
