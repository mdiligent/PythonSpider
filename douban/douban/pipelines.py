# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import codecs

class MovieItemPipeline(object):
    def __init__(self):
        self.file = codecs.open('../data/movie_item.json', 'w+', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()

class IDItemPipeline(object):
    def __init__(self):
        self.file = codecs.open('config/movie_id.out', 'w+', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        data = dict(item)
        keys = ', '.join(data.keys())
        values = data['movie_id'] + "\n"
        self.file.write(values)
        return item
    def spider_closed(self, spider):
        self.file.close()