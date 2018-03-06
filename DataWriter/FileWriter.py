# -*- coding: utf-8 -*-
import codecs
import json
import os
from DataWriter.BaseWriter import BaseWriter


class FileWriter(BaseWriter):
    save_path = None

    def __init__(self, path, name):
        if path is not None:
            self.save_path = os.path.join(path, name)
        else:
            self.save_path = name

    def write_data(self, page, data):
        page_path = self.save_path + str(page)
        with codecs.open(page_path, 'a', encoding="utf-8") as f:
            data = ','.join([k + "=" + v for k, v in data.items()])
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
