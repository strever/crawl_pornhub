# coding: utf-8

from scrapy import Request
from scrapy.spiders import CrawlSpider
from lib.proxy import Proxy


class PullProxySpider(CrawlSpider):
    name = "pull_proxy"
    allowed_domains = None
    start_urls = None
    pn = 3

    allowed_max_speed = 1.1

    def start_requests(self):
        # Proxy.del_all()
        urls = {
            # 'cybersyndrome': 'http://www.cybersyndrome.net/search.cgi?q=CN',
            # http://www.ip181.com/daili/1.html
            # goubanjia
            # 'pachong': 'http://pachong.org/'

            'xici': {
                'url': 'http://www.xicidaili.com/nn/{page}',
                'pn': self.pn,
                'callback': self.parse_xici
            },
            '66ip': {
                'url': 'http://www.66ip.cn/nmtq.php?getnum=50&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip',
                'pn': 1,
                'callback': self.parse_66ip
            },
            'kxdaili': {
                'url': 'http://www.kxdaili.com/dailiip/1/{page}.html#ip',
                'pn': self.pn,
                'callback': self.parse_kxdaili
            },
            'youdaili': {
                'url': 'http://www.youdaili.net/Daili/http/',
                'pn': 1,
                'callback': self.parse_youdaili
            },
            # 'proxylists': {
            #     'url': 'http://www.proxylists.net/cn_{page}_ext.html',
            #     'pn': self.pn,
            #     'callback': self.parse_proxylist
            # },
            'myproxy': {
                'url': 'https://www.my-proxy.com/free-proxy-list-{page}.html',
                'pn': self.pn,
                'callback': self.parse_myproxy
            },
        }

        for key, item in urls.items():
            for page in range(1, (item['pn']+1)):
                req = Request(item['url'].format(page=page), callback=item['callback'])
                yield req

    def parse_xici(self, response):
        for tr in response.xpath('//table[@id="ip_list"]//tr[position()>1]'):
            ip = tr.xpath('td[2]//text()').extract()
            port = tr.xpath('td[3]/text()').extract()
            speed = tr.xpath('td[7]/div[1]/@title').re(r'([\.\d]+)')
            protocal = tr.xpath('td[6]/text()').extract()
            if ip and port and speed and protocal:
                if float(speed[0]) < self.allowed_max_speed:
                    schema = 'http://'
                    if str(protocal[0]).strip().upper() == 'HTTP':
                        schema = 'http://'
                    if str(protocal[0]).strip().upper() == 'HTTPS':
                        schema = 'https://'

                    proxy = Proxy(schema, ip[0], port[0])
                    proxy.add()
                    return None

    def parse_kxdaili(self, response):
        for tr in response.xpath('//table/tbody/tr'):
            ip = tr.xpath('td[1]//text()').extract()
            port = tr.xpath('td[2]/text()').extract()
            speed = tr.xpath('td[5]/text()').re(r'([\.\d]+)')
            protocal = tr.xpath('td[4]/text()').extract()
            if ip and port and speed and protocal:
                if float(speed[0]) < self.allowed_max_speed:
                    schema = 'http://'
                    if str(protocal[0]).strip().upper() == 'HTTP':
                        schema = 'http://'
                    if str(protocal[0]).strip().upper() == 'HTTPS':
                        schema = 'https://'

                    proxy = Proxy(schema, ip[0], port[0])
                    proxy.add()
                    return None

    def parse_kuaidaili(self, response):
        for tr in response.xpath('//table/tbody/tr/[position()>1]'):
            ip = tr.xpath('td[1]//text()').extract()
            port = tr.xpath('td[2]/text()').extract()
            speed = tr.xpath('td[6]/text()').re(r'([\.\d]+)')
            protocal = tr.xpath('td[4]/text()').extract()
            if ip and port and speed and protocal:
                if float(speed[0]) < self.allowed_max_speed:
                    schema = 'http://'
                    if str(protocal[0]).strip().upper() == 'HTTP':
                        schema = 'http://'
                    if str(protocal[0]).strip().upper() == 'HTTPS':
                        schema = 'https://'

                    proxy = Proxy(schema, ip[0], port[0])
                    proxy.add()
                    return None

    def parse_goubanjia(self, response):
        for tr in response.xpath('//table[@class="table"]/tbody/tr'):
            ip = tr.xpath('td[1]//string(.)').extract()
            speed = tr.xpath('td[6]/text()').re(r'([\.\d]+)')
            protocal = tr.xpath('td[3]/a/text()').extract()
            if ip and speed and protocal:
                arr = str.split(':')
                if len(arr) > 1 and float(speed[0]) < self.allowed_max_speed:
                    schema = 'http://'
                    if str(schema[0]).strip().upper() == 'HTTP':
                        schema = 'http://'
                    if str(schema[0]).strip().upper() == 'HTTPS':
                        schema = 'https://'

                    proxy = Proxy(schema, arr[0], arr[1])
                    proxy.add()
                    return None

    def parse_myproxy(self, response):
        proxies = response.xpath('//p').re(r'(\d+\.\d+\.\d+\.\d+:\d+)#CN')
        for proxy_str in proxies:
            arr = proxy_str.split(':')
            if len(arr) > 1:
                proxy = Proxy('http://', arr[0], arr[1])
                proxy.add()

        return None

    def parse_cybersyndrome(self, response):
        for tr in response.xpath('//table/tbody/tr[position()>1]'):
            proxy_str = tr.xpath('td[2]//text()').extract_first()
            print(proxy_str)
            if proxy_str:
                arr = proxy_str.strip().split(':')
                if len(arr)>1:
                    proxy = Proxy('http://', arr[0], arr[1])
                    proxy.add()

        return None

    def parse_pachong(self, response):
        for tr in response.xpath('//table/tbody/tr[position()>1]'):
            ip = tr.xpath('td[2]/text()').extract_first()
            port = tr.xpath('td[3]').re(r'\d{2,4}')
            if ip and port:
                proxy = Proxy('http://', ip, port)
                proxy.add()

        return None

    def parse_66ip(self, response):
        proxies = response.xpath('/html/body').re(r'(\d+\.\d+\.\d+\.\d+:\d+)')
        for proxy_str in proxies:
            arr = proxy_str.split(':')
            if len(arr) > 1:
                proxy = Proxy('http://', arr[0], arr[1])
                proxy.add()

        return None

    def parse_youdaili(self, response):
        path = response.xpath('//div[@class="chunlist"]/ul/li[1]/p/a/@href').extract_first()
        for page in range(1, (self.pn+1)):
            url = path
            if page != 1:
                url = path.replace('.html', '_' + str(page) + '.html')
            req = Request(url, callback=self.parse_youdaili_detail)
            yield req

    def parse_youdaili_detail(self, response):
        for p in response.xpath('//div[@class="content"]/p'):
            str = p.xpath('text()').extract_first()
            ip = str.split(':')[0]
            port = str.split(':')[1].split('@')[0]
            if ip and port:
                proxy = Proxy('http://', ip, port)
                proxy.add()
        return None

    def closed(self, reason):
        count = Proxy.count()
        self.log('现有代理' + str(count) + '条')




