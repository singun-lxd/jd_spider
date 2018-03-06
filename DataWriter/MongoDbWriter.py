# -*- coding: utf-8 -*-
import pymongo

from DataWriter.BaseWriter import BaseWriter


class MongoDbWriter(BaseWriter):
    client = None
    db = None

    def __init__(self, url):
        self.client = pymongo.MongoClient(url)
        self.db = self.client.test

    def write_data(self, page, data):
        posts = self.db.posts
        result = posts.insert_one(data)
        print('post'.format(result.inserted_id))
