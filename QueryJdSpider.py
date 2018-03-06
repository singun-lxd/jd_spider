# -*- coding: utf-8 -*-
import thread
from pyquery import PyQuery
from JdBaseSpider import JdBaseSpider
from utils import get_html, HtmlGetter


# 使用pyquery的蜘蛛
class QueryJdSpider(JdBaseSpider):
    html_getter_list = []
    thread_lock = thread.allocate_lock()

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

    def acquire_html_getter(self, thread_id):
        """
        根据线程id获取html_getter
        多线程调用需要用锁保护
        :param thread_id:
        :return:
        """
        html_getter = None
        self.thread_lock.acquire()
        if thread_id > len(self.html_getter_list) - 1:
            html_getter = HtmlGetter()
            self.html_getter_list.insert(thread_id, html_getter)
        if html_getter is None:
            html_getter = self.html_getter_list[thread_id]
        self.thread_lock.release()
        return html_getter

    def get_page_details(self, page_url, thread_id):
        """
        解析每一个item项得到细节数据
        <li class="gl-item">
        :param page_url: 京东分类每一页的url
        :return: 该分类详情的generator
        """
        html_getter = self.acquire_html_getter(thread_id)
        html = html_getter.get_html(page_url)
        doc = PyQuery(html)
        items = doc(".gl-item").items()
        for item in items:
            item_id = item(".gl-i-wrap.j-sku-item").attr("data-sku")
            item_name = item(".p-name em").text()
            item_price = item(".J_price.js_ys").text()  #价格由js生成，所以必须使用HtmlGetter调用selenium解析
            item_url = item(".p-name a").attr("href")
            img_url = item(".p-img img").attr("src")
            if img_url is None:
                img_url = item(".p-img img").attr("data-lazy-img")
            yield {
                'item_id': item_id,
                'item_name': item_name,
                'item_price': item_price,
                'item_url': item_url,
                'img_url': img_url,
            }