from api import PluginParserBase, register_plugin, catch_stdout, is_valid_pathname


class Plugin(PluginParserBase):
    protocols = ["python", "pythons"]

    def rule_check(self, module_path):
        return self.protocol_check(module_path) and is_valid_pathname(self.remove_protocol(module_path))

    def get_data(self, module_path):
        protocol = self.get_protocol(module_path)

        try:
            with open(self.remove_protocol(module_path), "r") as f, catch_stdout() as s:
                data = f.read()
                exec(data)
            result = s.getvalue().strip()
            if protocol == "pythons":
                result = result.split()
            else:
                result = (result, )
            return result
        except Exception:
            return None


register_plugin(Plugin)
