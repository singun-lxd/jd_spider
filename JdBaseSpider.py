# -*- coding: utf-8 -*-
import threading
import time
from config import *

class JdBaseSpider:
    base_url = "https://list.jd.com/list.html"
    thread_count = 5

    def get_page_nums(self, main_url):
        return 0

    def get_page_details(self, page_url, thread_id):
        return ""

    def get_category_url(self, category_id):
        return "%s?cat=%s" % (self.base_url, category_id)

    def append_page_url(self, category_url, page):
        return "%s&page=%d" % (category_url, page)

    def parse_data(self, category_url, start_page, stop_page, thread_id):
        for page in range(start_page, stop_page + 1):
            #解析每一页的内容并输出
            page_url = self.append_page_url(category_url, page)
            print "start to parse url:" + page_url
            data = self.get_page_details(page_url, thread_id)
            for item in data:
                print ",".join(item)

    def execute(self):
        while True:
            #拿到总页码数
            category_id = ("670", "671", "672")
            category_url = self.get_category_url(",".join(category_id))
            print "start main url:" + category_url
            pages = self.get_page_nums(category_url)
            if pages is None:
                print "failed to parse pages"

            page_each_thread = pages / self.thread_count
            thread_list = []
            #每个线程执行一部分的解析工作
            for thread_id in range(0, self.thread_count):
                start = page_each_thread * thread_id + 1
                stop = pages + 1
                if thread_id < self.thread_count - 1:
                    stop = page_each_thread * (thread_id + 1) + 1
                t = threading.Thread(target=self.parse_data, args=(category_url, start, stop, thread_id))
                t.setDaemon(True)
                thread_list.append(t)
                t.start()

            #等待线程执行结束
            for t in thread_list:
                t.join()

            time.sleep(SLEEP_TIME)