from glimmer.api import PluginParserBase, register_plugin, CONFIG, ParserExceptions, cyberspace

from urllib import parse


class Plugin(PluginParserBase):
    protocols = ["zoomeye"]

    def rule_check(self, module_path):
        return self.protocol_check(module_path)

    def get_data(self, module_path):
        parsed = parse.urlparse(module_path)
        config = CONFIG.base.configuration
        key = parsed.username if parsed.username else config.zoomeye.get(
            "key", "")
        if not key:
            raise ParserExceptions.CyberSpace.APIKeyError("Missing key")
        params = parse.parse_qs(parsed.query)
        self.client = cyberspace.ZoomeyeClient(key)
        if "q" not in params:
            raise ParserExceptions.CyberSpace.Base("Missing query params: q")
        query_str = parse.unquote_plus(params["q"][0])
        max_page = int(parse.unquote_plus(
            params["max_page"][0])) if "max_page" in params else 1
        resources = parse.unquote_plus(
            params["resources"][0]) if "resources" in params else "host"
        fields = "ip,port"
        data = []
        for ip, port in self.client.query(query_str, max_page, resources, fields):
            data.append(
                    cyberspace.get_url_by_ip_port_domain(ip, port))
        return data

    def destruct(self):
        if (hasattr(self, "client")):
            del self.client


register_plugin(Plugin)
