from glimmer.api import PocBase, POC_TYPE, session
from urllib import parse


known_files = (
    '00changelog.i',
    'dirstate',
    'requires',
    'branch',
    'branchheads.cache',
    'last-message.txt',
    'tags.cache',
    'undo.branch',
    'undo.desc',
    'undo.dirstate',
    'store/00changelog.i',
    'store/00changelog.d',
    'store/00manifest.i',
    'store/00manifest.d',
    'store/fncache',
    'store/undo',
    '.hgignore'
)


class Poc(PocBase):
    """
        this poc will check if target website exist .hg source leak
    """
    vulid = "4"
    type = POC_TYPE.CODE_DISCLOSURE
    version = "1.0"
    authors = ['Longlone']
    references = ["https://github.com/kost/dvcs-ripper"]
    name = ".hg code leak"
    appName = "Mercurial"
    appVersion = "all"

    def check(self, url, **kwargs):
        target_url = parse.urljoin(url, ".hg") + "/"
        hit_urls = []

        res = session.get(target_url)
        status = 1
        pre_status = 0 if res.status_code == 403 else 1
        if not pre_status:
            for f in known_files:
                t_url = parse.urljoin(target_url, f)
                res = session.get(t_url)
                if res.status_code == 200:
                    status = 0
                    hit_urls.append(t_url)
                    break
        if not status:
            msg = "exist .hg source leak"
        elif not pre_status:
            msg = "maybe exist .hg source leak"
        else:
            msg = "not exist .hg source leak"
        result = {
            "url": url,
            "status": status,
            "msg": msg,
            "hit_urls": hit_urls,
            "extra": {
            }
        }
        return result
