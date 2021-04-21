import base64
import json
from urllib.parse import urlencode
import requests

from glimmer.libs.core.exceptions import ParserExceptions


class FofaClient:
    def __init__(self, email, key):
        self.email = email
        self.key = key
        self.base_url = "https://fofa.so"
        self.search_api_url = "/api/v1/search/all"
        self.login_api_url = "/api/v1/info/my"
        self.get_userinfo()  # check email and key

    def get_userinfo(self):
        api_full_url = "%s%s" % (self.base_url, self.login_api_url)
        param = {"email": self.email, "key": self.key}
        res = self.__http_get(api_full_url, param)
        return json.loads(res)

    def get_data(self, query_str, page=1, fields=""):
        res = self.get_json_data(query_str, page, fields)
        return json.loads(res)

    def get_json_data(self, query_str, page=1, fields=""):
        api_full_url = "%s%s" % (self.base_url, self.search_api_url)
        param = {"qbase64": base64.b64encode(
            query_str.encode()), "email": self.email, "key": self.key,
            "page": page, "fields": fields}
        res = self.__http_get(api_full_url, param)
        return res

    def query(self, query_str, max_page=1, fields=""):
        """
        support fields:

            host title ip domain port country province city country_name header server protocol banner cert isp as_number as_organization latitude longitude structinfo
        """
        if max_page < 1:
            return
        for page in range(1, max_page+1):
            data = self.get_data(query_str, page=page,
                                 fields=fields)["results"]
            yield data

    def query_ipc(self, ip_csegment="", max_page=1, fields='ip,port'):
        """
        support fields:

            host title ip domain port country province city country_name header server protocol banner cert isp as_number as_organization latitude longitude structinfo
        """
        return self.query(f'ip="{ip_csegment}"', max_page, fields)

    def __http_get(self, url, param):
        param = urlencode(param)
        url = "%s?%s" % (url, param)
        try:
            req = requests.get(url)
            res = req.text
        except requests.HTTPError as e:
            raise ParserExceptions.CyberSpace.HTTPError(e) from e
        return res
