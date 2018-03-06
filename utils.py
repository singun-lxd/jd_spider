# -*- coding: utf-8 -*-

import requests

def get_html(url, data=None):
    '''
    :param url:请求的url地址
    :param data: 请求的参数
    :return: 返回网页的源码html
    '''
    response = requests.get(url, data)
    return response.text