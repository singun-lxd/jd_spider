# -*- coding: utf-8 -*-

import time
from config import *

class JdBaseSpider:
    base_url = "https://list.jd.com/list.html"

    def get_page_nums(self, main_url):
        return 0

    def get_page_details(self, page_url):
        return ""

    def get_category_url(self, category_id):
        return "%s?cat=%s" % (self.base_url, category_id)

    def append_page_url(self, category_url, page):
        return "%s&page=%d" % (category_url, page)

    def execute(self):
        while True:
            category_id = ("670", "671", "672")
            category_url = self.get_category_url(",".join(category_id))
            print "start main url:" + category_url
            pages = self.get_page_nums(category_url)
            if pages is None:
                print "failed to parse pages"

            for page in range(1, pages + 1):
                page_url = self.append_page_url(category_url, page)
                print "start to parse url:" + page_url
                data = self.get_page_details(page_url)
                for item in data:
                    print "%s,%s,%s,%s,%s" % item

            print "parse finish"
            time.sleep(SLEEP_TIME)