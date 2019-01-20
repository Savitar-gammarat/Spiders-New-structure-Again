from config import FuncConfig as fc
from logger import Logger
import requests


class Req(object):  #类传入参数start_url，可选参数headers,是否使用代理proxy=False或其他值,

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
    }
    proxies = {
        'http': 'http://localhost:8123',
        'https': 'https://localhost:8123'
    }

    def __init__(self, url, headers=headers, proxy=False, params=False, cookies=False):
        self.url = url
        self.headers = headers
        self.proxy = proxy
        self.params = params
        self.cookies = cookies

    def get_select(self):
        response = None
        if type(self.headers) != dict:
            Logger().setLogger(fc.log_path, 2, "headers' type should be dict")
        elif type(self.proxy) != bool:
            Logger().setLogger(fc.log_path, 2, "proxy's type should be bool")
        else:
            if not self.proxy:
                if not self.params:
                    if not self.cookies:
                        try:
                            response = requests.get(self.url, headers=self.headers, timeout=10)
                        except:
                            Logger().setLogger(fc.log_path, 4, "Failed to requests webpage, error type:1, url is " + self.url)
                    else:
                        try:
                            response = requests.get(self.url, headers=self.headers, cookies=self.cookies, timeout=10)
                        except:
                            Logger().setLogger(fc.log_path, 4, "Failed to requests webpage, error type:2, url is " + self.url)
                else:
                    if not self.cookies:
                        try:
                            response = requests.get(self.url, headers=self.headers, params=self.params, timeout=10)
                        except:
                            Logger().setLogger(fc.log_path, 4, "Failed to requests webpage, error type:3, url is " + self.url)
                    else:
                        try:
                            response = requests.get(self.url, headers=self.headers, params=self.params,
                                                    cookies=self.cookies, timeout=10)
                        except:
                            Logger().setLogger(fc.log_path, 4, "Failed to requests webpage, error type:4, url is " + self.url)
            else:
                if not self.params:
                    if not self.cookies:
                        try:
                            response = requests.get(self.url, headers=self.headers, proxies=self.proxies, timeout=15)
                        except:
                            Logger().setLogger(fc.log_path, 4, "Failed to requests webpage, error type:5, url is " + self.url)
                    else:
                        try:
                            response = requests.get(self.url, headers=self.headers, proxies=self.proxies, cookies=self.cookies, timeout=15)
                        except:
                            Logger().setLogger(fc.log_path, 4, "Failed to requests webpage, error type:6, url is " + self.url)
                else:
                    if not self.cookies:
                        try:
                            response = requests.get(self.url, headers=self.headers, proxies=self.proxies, params=self.params, timeout=15)
                        except:
                            Logger().setLogger(fc.log_path, 4, "Failed to requests webpage, error type:7, url is " + self.url)
                    else:
                        try:
                            response = requests.get(self.url, headers=self.headers, proxies=self.proxies, params=self.params, cookies=self.cookies, timeout=15)
                        except:
                            Logger().setLogger(fc.log_path, 4, "Failed to requests webpage, error type:8, url is " + self.url)

            return response


def xpath_out(list):     #将由xpath选取后得到的list跳出为str或None
    if list == []:
        str = None
    elif list == None:
        str = None
    else:
        str = list[0].encode('utf8').decode('utf8')
    return str

def css_out(list):     #将由xpath选取后得到的list跳出为str或None
    if list == []:
        str = None
    elif list == None:
        str = None
    else:
        str = list[0]
    return str
