# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from CrawlLaGou.items import ArticleItemLoader, CrawllagouItem
from CrawlLaGou.utils.common import *
import datetime

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules =(
        Rule(LinkExtractor(allow='zhaopin/.*'), follow=True),
        Rule(LinkExtractor(allow='gongsi/j\d+.html'),follow=True),
        Rule(LinkExtractor(allow='jobs/\d+.html'), callback='parse_job', follow=True),
    )

    def parse_job(self, response):
        # 对拉勾网的具体职位进行解析，提取字段
        item_loader = ArticleItemLoader(item=CrawllagouItem, response=response)
        item_loader.add_css('title', '.job-name::attr(title)')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_ma5(response.url))
        item_loader.add_xpath('salary_numb', '//dd[@class="job_request"]/p/span[1]/text()')
        item_loader.add_xpath('work_city', '//dd[@class="job_request"]/p/span[2]/text()')
        item_loader.add_xpath('work_years', '//dd[@class="job_request"]/p/span[3]/text()')
        item_loader.add_xpath('educational', '//dd[@class="job_request"]/p/span[4]/text()')
        item_loader.add_xpath('work_type', '//dd[@class="job_request"]/p/span[5]/text()')
        item_loader.add_css('publish_time', '.publish_time::text')
        item_loader.add_css('Position_temptation', '#job_detail dd.job-advantage p::text')
        item_loader.add_css('work_desc', '.job_bt div p::text')
        item_loader.add_css('work_addr', '.job-address.clearfix .work_addr')
        item_loader.add_css('company_name', '.job_company dt a img::attr(alt)')
        item_loader.add_css('company_url', '.job_company dt a::attr(href)')
        item_loader.add_css('tags', '.position-label.clearfix li::text')
        item_loader.add_value('crawl_time', datetime.datetime.now())
        work_item = item_loader.load_item()
        return work_item

