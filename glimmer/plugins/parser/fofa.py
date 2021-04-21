from glimmer.api import PluginParserBase, register_plugin, CONFIG, ParserExceptions, cyberspace

from urllib import parse


class Plugin(PluginParserBase):
    protocols = ["fofa"]

    def rule_check(self, module_path):
        return self.protocol_check(module_path)

    def get_data(self, module_path):
        parsed = parse.urlparse(module_path)
        config = CONFIG.base.configuration
        email = parsed.username if parsed.username else config.fofa.get(
            "email", "")
        key = parsed.password if parsed.password else config.fofa.get(
            "key", "")
        if not key or not email:
            raise ParserExceptions.CyberSpace.APIKeyError("Missing key / email")
        params = parse.parse_qs(parsed.query)
        self.client = cyberspace.FofaClient(email, key)
        if "q" not in params:
            raise ParserExceptions.CyberSpace.Base("Missing query params: q")
        query_str = parse.unquote_plus(params["q"][0])
        max_page = int(parse.unquote_plus(params["max_page"][0])) if "max_page" in params else 1
        fields = "ip,port,domain"
        data = []
        for result in self.client.query(query_str, max_page, fields):
            for ip, port, domain in result:
                data.append(
                        cyberspace.get_url_by_ip_port_domain(ip, port, domain))
        return data

    def destruct(self):
        if (hasattr(self, "client")):
            del self.client


register_plugin(Plugin)
