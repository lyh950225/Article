# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy.loader import ItemLoader
import scrapy
from w3lib.html import remove_tags
from scrapy.loader.processors import TakeFirst, MapCompose,Join
from CrawlLaGou.utils.common import *


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class CrawllagouItem(scrapy.Item):
    # 建立爬取具体页面的字段
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary_numb = scrapy.Field()
    work_city = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    educational = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    work_type = scrapy.Field()
    publish_time = scrapy.Field()
    Position_temptation = scrapy.Field()
    work_desc = scrapy.Field()
    work_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags,remove_comment_addr),
    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field(
        input_processor=Join(",")
    )
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                insert into lagou_work(title, url, url_object_id, salary_numb, work_city, work_years, educational, work_type, publish_time, Position_temptation, work_desc, work_addr, company_name, company_url, tags, crawl_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,) ON DUPLICATE KEY UPDATE salary=VALUES(salary), work_desc=VALUES(work_desc)
        """
        params = (
            self["title"], self["url"], self["url_object_id"], self["salary_numb"], self["work_city"], self["work_years"], self["educational"], self["work_type"], self["publish_time"], self["Position_temptation"], self["work_desc"], self["work_addr"], self["company_name"], self["company_url"], self["tags"], self["crawl_time"],
        )
        return insert_sql, params
