# -*- coding: utf-8 -*-
# import httplib2
import os
import json
import urllib

import httplib2

from util.decorators import *
from pathlib import Path
import requests


DEFAULT_CACHE_DIR = 'D:\\dev\\_workspace\\.cache'
if Path('D:\\dev').is_dir():
    os.makedirs(DEFAULT_CACHE_DIR, exist_ok=True)
    http = httplib2.Http(DEFAULT_CACHE_DIR)
else:
    http = httplib2.Http()


@retry(Exception, retry=10, default_result={})
def request(url, method='GET', params=None, headers={}, return_json=False, ):
    body = None
    if 'GET' == method and params is not None:
        url = url.format(**params)
    else:
        if params is not None:
            body = urllib.parse.urlencode(params)

    print('loading ', url)
    _, content = http.request(url, method, body, headers=headers)

    if return_json:
        return json.loads(content) if content else {}
    else:
        return content


def shorten_url(url):
    """
    生成短网址
    """
    response = requests.get(f'https://api.uomg.com/api/long2dwz?dwzapi=urlcn&url={url}')
    resp = json.loads(response.text)
    if resp['code'] == 1 and 'ae_url' in resp:
        return resp['ae_url']
    else:
        return url
