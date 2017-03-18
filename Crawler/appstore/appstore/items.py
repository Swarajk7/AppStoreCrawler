# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppstoreItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    rating = scrapy.Field()
    url = scrapy.Field()

class AppItem(scrapy.Item):
    product_id = scrapy.Field()
    ratings = scrapy.Field()
    reviews = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    