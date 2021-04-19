from api import PocBase, requests


class Poc(PocBase):
    """
        this is a demo
    """
    vulid = "292929"
    version = "1.0"
    authors = ['Longlone']
    references = [""]
    name = "demo"
    appName = "Unknown"
    appVersion = "1.0-2.0"

    def check(self, url, **kwargs):
        res = requests.get(url)
        result = {
            "url": url,
            "status": 0 if res.status_code == 200 else 1,
            "msg": "demo poc " + "success" if res.status_code == 200 else "failed",
            "extra": {
            }
        }
        return result
