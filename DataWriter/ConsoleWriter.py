# -*- coding: utf-8 -*-
from DataWriter.BaseWriter import BaseWriter

class ConsoleWriter(BaseWriter):
    def write_data(self, page, data):
        print ','.join([k + "=" + v for k, v in data.items()])