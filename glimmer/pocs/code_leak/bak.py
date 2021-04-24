from glimmer.api import PocBase, POC_TYPE, session
from urllib import parse


known_files = [
    'www.zip',
    'www.rar',
    'root.zip',
    'root.rar',
    'wwwroot.zip',
    'wwwroot.rar',
    'backup.zip',
    'backup.rar',
    'tar.zip',
    'tar.rar',
    'web.zip',
    'web.rar',
    'web.tgz',
    'web1.zip',
    'web1.rar',
    'code.zip',
    'code.rar',
]
known_exts = ['.rar', '.zip', '.7z', '.tar.gz', '.bak', '.old']


class Poc(PocBase):
    """
        this poc will check if target website exist backup file source leak
    """
    vulid = "8"
    type = POC_TYPE.CODE_DISCLOSURE
    version = "1.0"
    authors = ['Longlone']
    references = ["https://github.com/kost/dvcs-ripper"]
    name = "backup file source leak"
    appName = ""
    appVersion = ""

    def check(self, url, **kwargs):
        parsed = parse.urlparse(url)
        hostname = parsed.hostname
        known_files.extend((hostname + ext for ext in known_exts))
        status = 1
        exist_files = []
        for f in known_files:
            t_url = parse.urljoin(url, f)
            res = session.get(t_url)
            if res.status_code == 200:
                status = 0
                exist_files.append(f)
        if not status:
            msg = "exist backup files:" + ", ".join(exist_files)
        else:
            msg = "not exist backup file source leak"
        result = {
            "url": url,
            "status": status,
            "msg": msg,
            "hit_urls": [parse.urljoin(url, exist_file) for exist_file in exist_files],
            "extra": {
            }
        }
        return result
