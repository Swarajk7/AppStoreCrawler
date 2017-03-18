# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os


class AppstorePipeline(object):
    def __init__(self):
        self.ar = []
        self.uniqUrls = set()
        self.count = 0

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        file = open('items.json', 'w')
        json.dump(self.ar, file, indent=2)
        file.close()

    def process_item(self, item, spider):
        dictItem = dict(item)
        self.count = self.count + 1
        dictItem['Id'] = self.count
        if dictItem['url'] not in self.uniqUrls:
            self.ar.append(dictItem)
        self.uniqUrls.add(dictItem['url'])
        return item


class AppPipeline(object):
    def __init__(self):
        self.is_first = True

    def open_spider(self, spider):
        self.file = open(r'output\ITEMS.json', 'w')
        self.file.write('[' + "\n")

    def close_spider(self, spider):
        self.file.write(']' + "\n")
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        if not self.is_first:
            line = "," + line
        self.file.write(line)
        self.is_first = False
        with open(r'output\Review' + item['product_id'] + '.json', 'w') as fp:
            json.dump(dict(item), fp)
        return item
