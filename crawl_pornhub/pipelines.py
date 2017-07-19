# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

from lib.db import DB

class CrawlPornhubPipeline(object):
    def process_item(self, item, spider):
        if item['title'] and item['video_link']:
            sql = "INSERT INTO `pornhub_videos`(`title`, `thumb`, `duration`, `video_link`, `video_link_480p`) " \
                  "VALUES(%s, %s, %s, %s, %s)"
            #sql = DB.connect().conn.cursor().mogrify(sql, (item['province'], item['city'], item['district'], item['path'], item['amount'], item['page_num']))
            DB.connect().execute(sql, (item['title'], item['thumb'], item['duration'], item['video_link'], item['video_link_480p']))
            return item
        else:
            raise DropItem('item由于不完整被丢弃')
