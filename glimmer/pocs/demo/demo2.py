from api import PocBase, POC_TYPE, requests


class Poc(PocBase):
    """
        this is a demo2
    """
    vulid = "0"
    type = POC_TYPE.UNKNOWN
    version = "1.0"
    authors = ['Longlone']
    references = [""]
    name = "demo2"
    appName = ""
    appVersion = ""

    def check(self, url, **kwargs):
        res = requests.get(url)
        result = {
            "url": url,
            "status": 0 if res.status_code == 200 else 1,
            "msg": "demo2 poc " + ("success" if res.status_code == 200 else "failed"),
            "extra": {

            }
        }
        return result
