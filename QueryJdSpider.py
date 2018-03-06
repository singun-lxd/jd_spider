# -*- coding: utf-8 -*-

from pyquery import PyQuery
from JdBaseSpider import JdBaseSpider
from utils import get_html, HtmlGetter


# 使用pyquery的蜘蛛
class QueryJdSpider(JdBaseSpider):
    html_getter = HtmlGetter()

    def get_page_nums(self, main_url):
        """
        解析以下html，得到页码
        <span class="p-skip">
            <em>共<b>1111</b>页&nbsp;&nbsp;到第</em>
            ......
        </span>
        :param main_url: 京东分类页面主url
        :return: 该分类总共多少页
        """
        html = get_html(main_url)
        doc = PyQuery(html)
        page = doc(".p-skip em b")
        print "page number:" + page.text()
        return int(page.text())

    def get_page_details(self, page_url):
        """
        解析每一个item项得到细节数据
        <li class="gl-item">
        :param page_url: 京东分类每一页的url
        :return: 该分类详情的generator
        """
        html = self.html_getter.get_html(page_url)
        doc = PyQuery(html)
        items = doc(".gl-item").items()
        for item in items:
            item_id = item(".gl-i-wrap.j-sku-item").attr("data-sku")
            item_name = item(".p-name em").text()
            item_price = item(".J_price.js_ys").text()
            item_url = item(".p-name a").attr("href")
            img_url = item(".p-img img").attr("src")
            if img_url is None:
                img_url = item(".p-img img").attr("data-lazy-img")
            yield (item_id, item_name, item_price, item_url, img_url)