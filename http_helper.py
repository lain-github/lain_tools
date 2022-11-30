# -*- coding: utf-8 -*-
'''
http助手，对request模块的封装，方便上层使用。
'''
import requests
#from requests.sessions import session

# 超时设置（连接超时，读取超时），单位：秒
TIMEOUT = (1,5)
# 代理服务器
PROXIES = None

HEADERS = None
ENCODING = 'utf-8'

class HttpHelper(object):
    def __init__(self, encoding=ENCODING, timeout=TIMEOUT, proxies=PROXIES, headers=HEADERS):
        session=requests.session()
        if proxies:
            session.proxies=proxies
        if headers:
            session.headers.update(headers)

        self.session=session
        self.encoding=encoding
        self.timeout=timeout

    def request(self, method, url, **kwargs):
        # 确保timeout被设置
        if 'timeout' not in kwargs:
            kwargs['timeout']=self.timeout

        try:
            rsp=self.session.request(method, url, **kwargs)
        except Exception as ex:
            print('http %s error. url=%s, args=%s, ex=%s',
                  method, url, kwargs, ex, stack_info=True)
            return None

        if rsp.status_code >= 300 or rsp.status_code <= 100:
            print('http %s fail. url=%s, args=%s, status=%s, text=%s',
                  method, url, kwargs, rsp.status_code, rsp.text)
            return None

        rsp.encoding=self.encoding

        return rsp

    def get(self, url, **kwargs):
        rsp=self.request('GET', url, **kwargs)
        return rsp.text if rsp else None

    def post(self, url, **kwargs):
        rsp=self.request('POST', url, **kwargs)
        return rsp.text if rsp else None

    def download(self, url, **kwargs):
        '''下载，返回字节数组'''
        rsp=self.request('GET', url, **kwargs)
        return rsp.content if rsp else None

    def get_cookie(self, key):
        return self.session.cookies.get(key)

    def update_headers(self, headers):
        self.session.headers.update(headers)
'''
http=HttpHelper()
text=http.get('https://www.baidu.com/')
print(text)
'''