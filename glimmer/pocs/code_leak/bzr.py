from glimmer.api import PocBase, POC_TYPE, session
from urllib import parse


known_files = (
    'branch-format',
    'branch/branch.conf',
    'branch/format',
    'branch/last-revision',
    'branch/tags',
    'checkout/conflicts',
    'checkout/dirstate',
    'checkout/format',
    'checkout/merge-hashes',
    'checkout/views',
    'repository/format',
    'repository/pack-names'
)


class Poc(PocBase):
    """
        this poc will check if target website exist .bzr source leak
    """
    vulid = "7"
    type = POC_TYPE.CODE_DISCLOSURE
    version = "1.0"
    authors = ['Longlone']
    references = ["https://github.com/kost/dvcs-ripper"]
    name = ".bzr code leak"
    appName = "Bazaar"
    appVersion = "all"

    def check(self, url, **kwargs):
        target_url = parse.urljoin(url, ".bzr") + "/"
        hit_urls = []

        res = session.get(target_url)
        status = 1
        pre_status = 0 if res.status_code == 403 else 1
        if not pre_status:
            for f in known_files:
                t_url = parse.urljoin(target_url, f)
                res = session.get(t_url)
                if res.status_code == 200:
                    hit_urls.append(t_url)
                    status = 0
                    break
        if not status:
            msg = "exist .bzr source leak"
        elif not pre_status:
            msg = "maybe exist .bzr source leak"
        else:
            msg = "not exist .bzr source leak"
        result = {
            "url": url,
            "status": status,
            "msg": msg,
            "hit_urls": hit_urls,
            "extra": {
            }
        }
        return result
