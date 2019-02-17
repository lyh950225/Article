# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Article.items import LagouJobItemLoader, LagouJobItem
from Article.utils.common import get_ma5
from datetime import datetime

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        Rule(LinkExtractor(allow=('gongsi/\d+.html',)),follow=True),
        Rule(LinkExtractor(allow=('zhaopin/.*',)),follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_item', follow=True),
    )

    # def parse_start_url(self, response):
    #     return []
    #
    # def process_results(self, response, results):
    #     return results

    def parse_item(self, response):
        # 解析拉勾网的职位
        item_load = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_load.add_value('url', response.url)
        item_load.add_value('url_object_id', get_ma5(response.url))
        item_load.add_css('title', '.job-name::attr(title)')
        item_load.add_css('salary', '.job_request .salary::text')
        item_load.add_xpath('job_city', '//*[@class="job_request"]/p/span[2]/text()')
        item_load.add_xpath('education', '//*[@class="job_request"]/p/span[4]/text()')
        item_load.add_xpath('job_type', '//*[@class="job_request"]/p/span[5]/text()')
        item_load.add_xpath('job_exper', '//*[@class="job_request"]/p/span[3]/text()')
        item_load.add_css('tags', '.position-label .li::text')
        item_load.add_css('release_time', '.publish_time::text')
        item_load.add_css('job_seduce', '.job-advantage .advantage p::text')
        item_load.add_css('job_desc', '.job_bt .description .job-detail::text')
        item_load.add_css('company_name', '.job-name .company')
        item_load.add_css('company_url', '.job_company dt a::attr(href)')
        item_load.add_css('job_addr', '.work_addr')
        item_load.add_value('crawl_time', datetime.now())
        job_item = item_load.load_item()


        return job_item

