# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import pymongo
from scrapy.exceptions import DropItem
from pymongo import MongoClient


class MongoPipeline(object):
    
    collection_name = 'testjob'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = MongoClient("localhost", 27017)
        self.db = self.client["jobsearchengine"]
        self.testjob = self.db["testjob"]

    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        ## initializing spider
        ## opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        ## how to handle each post

        self.db[self.collection_name].insert(dict(item))
       
        logging.debug("Post added to MongoDB")
        return item

"""
class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = []

    def process_item(self, item, spider):
        if item["guid"] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.append(item['guid'])
            return item
"""