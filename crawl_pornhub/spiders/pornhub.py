# coding: utf-8
import scrapy
from scrapy import Request
from crawl_pornhub.items import CrawlPornhubItem
import re
from scrapy.selector import Selector
import json
from lib.log import Log
from scrapy.spiders import CrawlSpider


class PornhubSpider(CrawlSpider):
    name = 'pornhub'
    start_urls = None
    allowed_domains = None
    pornhub_domain = 'https://www.pornhub.com/'

    cmd_arg = None

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'ITEM_PIPELINES': {
            'crawl_pornhub.pipelines.CrawlPornhubPipeline': 400
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            #'crawl_pornhub.middlewares.RandomProxyMiddleware': 300,

            'crawl_pornhub.middlewares.RandomUserAgentMiddleware': 400,
            "crawl_pornhub.middlewares.CookiesMiddleware": 402,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 410,
        }
    }

    """归纳PornHub资源链接"""
    PH_TYPES = [
        '',
        'recommended',
        'video?o=ht',  # hot
        'video?o=mv',  # Most Viewed
        'video?o=tr'  # Top Rate
    ]

    def __init__(self, cmd_arg='demo', *a, **kw):
        super(PornhubSpider, self).__init__(*a, **kw)
        self.cmd_arg = cmd_arg

    def start_requests(self):
        self.log('-----------------------------------我要开始上天了-----------------------------')
        for porn_type in self.PH_TYPES:
            yield Request(url='https://www.pornhub.com/%s' % porn_type, callback=self.parse)

        pass

    def parse(self, response):
        self.log('抓取开始: %s ...' % response.url)
        Log.info('[crawling]' + response.url)

        divs = response.xpath('//div[@class="phimage"]')
        for div in divs:
            viewkey = re.findall('viewkey=(.*?)"', div.extract())
            if len(viewkey) > 0:
                yield Request(url='https://www.pornhub.com/embed/%s' % viewkey[0], callback=self.parse_info)
        # url_next = response.xpath(
        #     '//a[@class="orangeButton" and text()="Next "]/@href').extract()
        # if url_next:
        #     yield Request(url=self.pornhub_domain + url_next[0],
        #                   callback=self.parse_ph_key)


            # self.test = False
    def parse_info(self, response):
        self.log('抓取开始: %s ...' % response.url)
        Log.info('[crawling]' + response.url)
        porn_item = CrawlPornhubItem()
        selector = Selector(response)
        _ph_info = re.findall('flashvars_.*?=(.*?);\n', selector.extract())
        if len(_ph_info) > 0:
            _ph_info_json = json.loads(_ph_info[0])
            #Log.info(_ph_info_json)
            duration = _ph_info_json.get('video_duration')
            porn_item['duration'] = duration
            title = _ph_info_json.get('video_title')
            porn_item['title'] = title
            image_url = _ph_info_json.get('image_url')
            porn_item['thumb'] = image_url
            link_url = _ph_info_json.get('link_url')
            porn_item['video_link'] = link_url
            quality_480p = _ph_info_json.get('quality_480p')
            porn_item['video_link_480p'] = quality_480p
            yield porn_item