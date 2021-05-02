# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class MongoPipeline(object):
    collection_name = 'imdb'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        exists = self.db[self.collection_name].find_one({"title": dict(item)["title"]})
        if not exists:
            self.db[self.collection_name].insert_one(dict(item))
        return item


class MoviePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # Clean item
        for key in adapter:
            if adapter.get(key) and not isinstance(adapter[key], list):
                adapter[key] = adapter[key].strip()

            if adapter.get(key) and isinstance(adapter[key], list):
                adapter[key] = [value.strip() for value in adapter[key] if value != '|']

        # Money data types
        for key in ['budget','gross_usa','opening_weekend_usa','cumulative_gross']:
            if adapter.get(key) and re.match('\$[0-9]', adapter[key]):
                adapter[key] = int( adapter[key].strip('$').replace(',', '') ) 
        
        # Integer data types
        for key in ['rating_count']:
            if adapter.get(key) and adapter[key].replace(',', '').isdigit():
                adapter[key] = int(adapter[key].replace(',', ''))

        # Float data types
        if adapter.get('rating'):
            adapter['rating'] = float(adapter['rating'])

        # Transform summary
        if adapter.get('summary'):
            adapter['summary'] = ' '.join([s.strip() for s in adapter['summary']])
        
        return item
