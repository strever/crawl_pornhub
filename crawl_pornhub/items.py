# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlPornhubItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field(serializer=str)
    thumb = scrapy.Field(serializer=str)
    duration = scrapy.Field(serializer=int)
    video_link = scrapy.Field(serializer=str)
    video_link_480p = scrapy.Field(serializer=str)
    pass
