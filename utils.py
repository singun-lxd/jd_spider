# -*- coding: utf-8 -*-

import requests
from selenium import webdriver

def get_html(url, data=None):
    '''
    :param url:请求的url地址
    :param data: 请求的参数
    :return: 返回网页的源码html
    '''
    response = requests.get(url, data)
    return response.text

class HtmlGetter:
    browser = None

    def __init__(self):
        pass
        #self.browser = webdriver.Chrome()

    def get_html(self, url):
        if self.browser is None:
            self.browser = webdriver.Chrome()
        self.browser.get(url)
        return self.browser.find_element_by_xpath("//*").get_attribute("outerHTML")

    def __del__(self):
        if self.browser is not None:
            self.browser.close()