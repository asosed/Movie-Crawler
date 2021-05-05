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
                adapter[key] = list(set([value.strip() for value in adapter[key] if value != '|']))

        # # Money data types
        # for key in ['budget','opening_weekend_usa','cumulative_gross']:
        #     if adapter.get(key) and re.match('\d+', adapter[key]):
        #         extract = re.search('\d+([,][\d]+)?([,][\d]+)?').group(0)
        #         adapter[key] = int( adapter[key].replace(',', '') ) 
        
        # Integer data types
        for key in ['rating_count','opening_weekend_usa','cumulative_gross','budget']:
            if adapter.get(key) and re.search('\d+', adapter[key]):
                extract = re.search('\d+([,][\d]+)?([,][\d]+)?', adapter[key]).group(0)
                adapter[key] = int(extract.replace(',', ''))

        # Float data types
        for key in ['rating', 'gross_usa']:
            if adapter.get(key) and re.search('\d+', adapter[key]):
                extract = re.search('\d+(,\d{3})*(\.\d*)?', adapter[key]).group(0)
                adapter[key] = float(extract.replace(',',''))

        # Clean genres
        if adapter.get('genres') and not isinstance(adapter['genres'], list):
            adapter['genres'] = [re.sub('\n','',s).strip() for s in adapter['genres'].split(',')]
        

        return item
