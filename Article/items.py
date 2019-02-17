# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import datetime
import re
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags
from Article.utils.common import get_ma5
from Article.utils.common import extract_nums
from Article.settings import SQL_DATE_FORMAT, SQL_DATETIME_FORMAT

class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value + "-jobbole"


def date_convert(value):
        try:
            create_time = datetime.datetime.strptime(value, "%Y/%m/%d").date()
        except Exception as e:
            create_time = datetime.datetime.now().date()
        return create_time


def get_nums(value):
    match_re = re.match(".*?(\d+).*?", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def remove_comment_tags(value):
    # 去掉TAG中提取的评论
    if "评论" in value:
        return ""
    else:
        return value


def return_value(value):
    return value


class ArticleItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(add_jobbole)
    )
    create_time = scrapy.Field(
        input_processor=MapCompose(date_convert)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    faves_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tag_list = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    contens = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                            insert into jobbole (title, url, create_time, faves_nums)
                            VALUES (%s, %s, %s, %s)
                            """
        params = (self['title'], self['url'], self['create_time'], self['faves_nums'])
        return insert_sql, params


# class ZhihuQuestionItem(scrapy.item):
#     # 知乎问题的Item
#     zhihu_id = scrapy.Field()
#     topics = scrapy.Field()
#     url = scrapy.Field()
#     title = scrapy.Field()
#     contents = scrapy.Field()
#     answer_nums = scrapy.Field()
#     crawl_time = scrapy.Field()
#
#     def get_insert_sql(self):
#         # 插入知乎Question的SQL语句
#         insert_sql = """
#                 insert into zhihu_question(zhihu_id, topics, url, title, contents, ,answer_nums, crawl_time)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s)
#                 ON DUPLICATE KEY UPDATE contents = values (contents)
#         """
#         # 由于ItemLoader返回的是列表，所以插入SQL的参数要先从列表中提取出来
#         # 由于没有写知乎的爬取规则，这里仅仅作为代码参考
#         zhihu_id = int(self['zhihu_id]'[0]) #在数据库设计表中是INT类型
#         topics = ",".join(self["topics"])  # 用逗号作为分隔将TOPICS列表中的字符转化为一个字符串
#         url = self["url"][0]
#         answer_nums = extract_nums("".join(self["answer_nums"]))
#         contents = extract_nums("".join(self["contents"]))
#         crawl_time = datetime.datetime.now().strptime(SQL_DATETIME_FORMAT)
#
#         params = (zhihu_id, topics, url, answer_nums, contents, answer_nums, crawl_time)
#         return insert_sql, params

class LagouJobItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class LagouJobItem(scrapy.Item):
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field()
    job_addr = scrapy.Field()
    job_exper = scrapy.Field()
    education = scrapy.Field()
    job_type = scrapy.Field()
    release_time = scrapy.Field()
    job_seduce = scrapy.Field()
    job_desc = scrapy.Field(
        input_processor=MapCompose(remove_tags)
    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field(
        input_processor=Join(",")
    )
    crawl_time = scrapy.Field()

