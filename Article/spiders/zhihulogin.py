# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings


class Zhihu_Cookies_Login(scrapy.Spider):
    name = 'zhihulogin'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        'Host' : 'www.zhihu.com',
        'Connection': 'keep - alive'
    }
    cookie = settings['COOKIES']

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], headers=self.headers, cookies=self.cookie, method='POST')

    def parse(self, response):
        print(response.body)
