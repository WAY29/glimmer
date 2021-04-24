from glimmer.api import PocBase, POC_TYPE, session
from urllib import parse
import re


class Poc(PocBase):
    """
        this poc will check if target exist jenkins unauthorized access
    """
    vulid = "14"
    type = POC_TYPE.UNAUTHORIZED_ACCESS
    version = "1.0"
    authors = ['Longlone']
    references = []
    name = "jenkins unauth access"
    appName = "Redis"
    appVersion = "4.x/5.x"

    def check(self, url, **kwargs):
        status = 1
        parsed = list(parse.urlparse(url))
        parsed[1] = re.sub(r":\d+", ":8080", parsed[1]) if ":" in parsed[1] else parsed[1] + ":8080"
        parsed[2] = "/manage"
        default_url = parse.urlunparse(parsed)
        target_url = url
        for target_url in (url, default_url):
            manage_url = parse.urljoin(target_url, "manage")
            res = session.get(manage_url)
            if res.request.url == manage_url and "Jenkins [Jenkins]</title>" in res.text:
                status = 0
                target_url = manage_url
                break

        if not status:
            msg = "exist jenkins unauthorized access"
        else:
            msg = "not exist jenkins unauthorized access"

        result = {
            "url": url,
            "status": status,
            "msg": msg,
            "hit_urls": [target_url],
            "extra": {
            }
        }
        return result
