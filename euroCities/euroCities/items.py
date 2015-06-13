# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CityListItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()

class CityLinkItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()

class CityItem(scrapy.Item):
    city = scrapy.Field()
    country = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
