from glimmer.api import PluginParserBase, register_plugin, requests, is_valid_url
from urllib import parse


class Plugin(PluginParserBase):
    protocols = ["repo"]

    def get_raw_urls(self, module_path):
        module_path = self.remove_protocol(module_path)
        if module_path.endswith("/"):
            res = requests.get(
                "https://gitee.com/guuest/glimmer_pocs/raw/master/dir_struct.txt")
            return [parse.urljoin("https://gitee.com/guuest/glimmer_pocs/raw/master/", path) for path in res.text.split() if path.startswith(module_path)]
        else:
            module_path = module_path if module_path.endswith(
                ".py") else module_path + ".py"
            return (parse.urljoin("https://gitee.com/guuest/glimmer_pocs/raw/master/", module_path), )

    def rule_check(self, module_path):
        return self.protocol_check(module_path) and all(is_valid_url(path) for path in self.get_raw_urls(module_path))

    def get_data(self, module_path):
        try:
            results = []
            for module_url in self.get_raw_urls(module_path):
                res = requests.get(module_url, verify=False)
                results.append(res.text)
            return results
        except Exception:
            return ()


register_plugin(Plugin)
