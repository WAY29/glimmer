import ssl
from urllib3 import disable_warnings

from requests.models import Request
from requests.sessions import Session
from requests.sessions import merge_setting, merge_cookies
from requests.cookies import RequestsCookieJar
from requests.utils import get_encodings_from_content

import logging
from glimmer.libs.logger import logger
from glimmer.libs.core.config import CONFIG


def session_request(self, method, url,
                    params=None, data=None, headers=None, cookies=None, files=None, auth=None,
                    timeout=None,
                    allow_redirects=True, proxies=None, hooks=None, stream=None, verify=False, cert=None, json=None):
    # Create the Request
    conf = CONFIG.base.get("request", {})
    merged_cookies = merge_cookies(merge_cookies(RequestsCookieJar(), self.cookies),
                                   cookies or (conf.get("cookies", {})))

    req = Request(
        method=method.upper(),
        url=url,
        headers=merge_setting(
            headers, conf.get("headers", {})),
        files=files,
        data=data or {},
        json=json,
        params=params or {},
        auth=auth,
        cookies=merged_cookies,
        hooks=hooks,
    )
    prep = self.prepare_request(req)

    proxies = proxies or conf.get("proxies", {})

    settings = self.merge_environment_settings(
        prep.url, proxies, stream, verify, cert
    )

    # Send the request.
    send_kwargs = {
        'timeout': timeout,
        'allow_redirects': allow_redirects,
    }
    send_kwargs.update(settings)
    resp = self.send(prep, **send_kwargs)

    if resp.encoding == 'ISO-8859-1':
        encodings = get_encodings_from_content(resp.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = resp.apparent_encoding

        resp.encoding = encoding

    return resp


def _patch_session():
    Session.request = session_request


def _remove_ssl_verify():
    ssl._create_default_https_context = ssl._create_unverified_context


def _upgrade_urllib3_logger_level():
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def _disable_warnings():
    disable_warnings()


def patch_request():
    logger.info("patch_requests: patch something about requests")
    _disable_warnings()
    _remove_ssl_verify()
    _upgrade_urllib3_logger_level()
    _patch_session()
