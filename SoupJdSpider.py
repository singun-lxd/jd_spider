# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from JdBaseSpider import JdBaseSpider
from utils import get_html, HtmlGetter

# 使用BeautifulSoup的蜘蛛
class SoupJdSpider(JdBaseSpider):
    html_getter = None

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
        soup = BeautifulSoup(html, "lxml")
        page = soup.select(".p-skip em b")
        print "page number:" + page.get_text()
        return int(page.get_text())

    def check_html_getter(self):
        if self.html_getter is None:
            self.html_getter = HtmlGetter()

    def get_page_details(self, page_url):
        """
        解析每一个item项得到细节数据
        <li class="gl-item">
        :param page_url: 京东分类每一页的url
        :return: 该分类详情的generator
        """
        self.check_html_getter()
        html = self.html_getter.get_html(page_url)
        soup = BeautifulSoup(html, "lxml")
        items = soup.select(".gl-item")
        for item in items:
            item_id = item.select(".gl-i-wrap.j-sku-item").attrs("data-sku")
            item_name = item.select(".p-name em").get_text()
            item_price = item.select(".J_price.js_ys").get_text()
            item_url = item.select(".p-name a").attrs("href")
            img_url = item.select(".p-img img").attrs("src")
            if img_url is None:
                img_url = item.select(".p-img img").attrs("data-lazy-img")
            yield (item_id, item_name, item_price, item_url, img_url)