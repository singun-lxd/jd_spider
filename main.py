# -*- coding: utf-8 -*-
from DataWriter.FileWriter import FileWriter
from QueryJdSpider import QueryJdSpider


if __name__ == '__main__':
    spider = QueryJdSpider(FileWriter(None, "result_page_"))
    spider.execute()
