from glimmer.api import PluginParserBase, register_plugin, CONFIG, ParserExceptions, cyberspace

from urllib import parse


class Plugin(PluginParserBase):
    protocols = ["shodan"]

    def rule_check(self, module_path):
        return self.protocol_check(module_path)

    def get_data(self, module_path):
        parsed = parse.urlparse(module_path)
        config = CONFIG.base.configuration
        key = parsed.username if parsed.username else config.shodan.get(
            "key", "")
        if not key:
            raise ParserExceptions.CyberSpace.APIKeyError("Missing key")
        params = parse.parse_qs(parsed.query)
        self.client = cyberspace.ShodanClient(key)
        if "q" not in params:
            raise ParserExceptions.CyberSpace.Base("Missing query params: q")
        query_str = parse.unquote_plus(params["q"][0])
        max_page = int(parse.unquote_plus(
            params["max_page"][0])) if "max_page" in params else 1
        limit = parse.unquote_plus(params["limit"][0]) if "limit" in params else 1
        fields = "ip,port,domains"
        data = []
        for ip, port, domains in self.client.query(query_str, max_page, limit, fields):
            domain = domains[0] if len(domains) > 0 else ""
            data.append(
                cyberspace.get_url_by_ip_port_domain(ip, port, domain))
        return data

    def destruct(self):
        if (hasattr(self, "client")):
            del self.client


register_plugin(Plugin)
