# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class TorrentPipeline(object):
    def open_spider(self, spider):
        self.mongo_client = pymongo.MongoClient()

    def process_item(self, item, spider):
        self.mongo_client.torrents.ohyes.insert_one(item)
        return item

    def close_spider(self, spider):
        self.mongo_client.close()