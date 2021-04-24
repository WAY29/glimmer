from glimmer.api import PocBase, POC_TYPE, session
from urllib import parse


class Poc(PocBase):
    """
        this poc will check if target website exist WEB-INF source leak
    """
    vulid = "5"
    type = POC_TYPE.CODE_DISCLOSURE
    version = "1.0"
    authors = ['Longlone']
    references = []
    name = "WEB-INF code leak"
    appName = "Java web"
    appVersion = "all"

    def check(self, url, **kwargs):
        target_url = parse.urljoin(url, "WEB-INF/web.xml")

        res = session.get(target_url)
        status = 0 if res.status_code == 403 else 1
        if not status:
            msg = "exist WEB-INF source leak"
        else:
            msg = "not exist WEB-INF source leak"
        result = {
            "url": url,
            "status": status,
            "msg": msg,
            "hit_urls": target_url,
            "extra": {
            }
        }
        return result
