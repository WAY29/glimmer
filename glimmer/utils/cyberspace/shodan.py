import shodan
from glimmer.libs.core.exceptions import ParserExceptions


class ShodanClient:
    def __init__(self, key):
        self.key = key
        self.api = shodan.Shodan(key)

    def query(self, query_str, max_page=1, limit=None, fields="", minify=True):
        """
        support fields:

        asn data ip(ip_str) ipv6 port timestamp hostnames domains location(Object) country(location.country_name) opts org isp os transport link title html product version devicetype info cpe

        https://developer.shodan.io/api/banner-specification
        """
        try:
            for page in range(1, max_page+1):
                data = self.api.search(query_str, page, limit, minify=minify)
                if fields == "":
                    yield data
                else:
                    for result in data['matches']:
                        yield [_getinfo(result, field) for field in fields.split(",")]
        except shodan.APIError as e:
            raise ParserExceptions.CyberSpace.APIError(e) from e


def _getinfo(data: dict, attr=''):
    if attr == "ip":
        return data["ip_str"]
    elif attr == "country":
        return data["location"]["country_name"]
    return data[attr]
