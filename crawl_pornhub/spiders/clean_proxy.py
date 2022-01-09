#  coding: utf-8
import scrapy
from scrapy import Request

from lib.proxy import Proxy


class CleanProxySpider(scrapy.Spider):
    name = "clean_proxy"
    allowed_domains = None
    start_urls = None

    try_times = 3

    def start_requests(self):
        proxies = Proxy.all()
        for i in range(1, (self.try_times+1)):
            for proxy in proxies:
                req = Request('http://httpbin.org/get?show_env=1', dont_filter=True)
                proxy = proxy.decode('utf-8')
                req.meta['proxy'] = proxy
                req.meta['dont_retry'] = True
                req.meta['download_timeout'] = 5
                yield req

    def parse(self, response):
        proxy = response.meta['proxy']
        Proxy.update_score(proxy)
        return None

    def closed(self, reason):
        Proxy.remove_invalid()
        print(Proxy.all_valid())

