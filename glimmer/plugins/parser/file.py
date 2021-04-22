from glimmer.api import PluginParserBase, register_plugin, is_valid_pathname, base64_decode, check_if_base64


class Plugin(PluginParserBase):
    protocols = ["file", "files"]

    def rule_check(self, module_path):
        return self.protocol_check(module_path) and is_valid_pathname(self.remove_protocol(module_path))

    def get_data(self, module_path):
        protocol = self.get_protocol(module_path)
        try:
            module_path = self.remove_protocol(module_path)
            with open(module_path, "r") as f:
                result = f.read()
            if protocol == "files":
                result = result.split()
                result = [base64_decode(r) if check_if_base64(
                    r) else r for r in result]
                return result
            else:
                return (result, )
        except Exception:
            return ()


register_plugin(Plugin)
