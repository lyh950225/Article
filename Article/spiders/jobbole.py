# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse
from Article.items import JobboleArticleItem, ArticleItemLoader
from Article.utils.common import get_ma5
from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1.抓取所有的页面url,并且进行解析
        2.抓取下一页里包含的网页，并且进行解析
        :param response:
        :return:
        """
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css('img::attr(src)').extract_first("")
            post_url = post_node.css('::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url" : image_url}, callback=self.parse_detail)

        next_urls = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_urls:
            Request(url=parse.urljoin(response.url, next_urls), callback=self.parse)

    def parse_detail(self, response):
        """
        对页面文章进行解析
        :param response:
        :return:
        """
        # article_item = JobboleArticleItem()
        # # css选择器进行定位
        front_image_url = response.meta.get("front_image_url", "") # 文章封面图
        # title = response.css('.entry-header h1::text').extract()[0]
        # create_time = response.css('.entry-meta-hide-on-mobile::text').extract()[0].strip().replace("·", "").strip()
        # praise_nums = response.css('span.vote-post-up h10::text').extract()[0]
        # faves_nums = response.css('span.bookmark-btn::text').extract()[0]
        # match_re = re.match(".*?(\d+).*?", faves_nums)
        # if match_re:
        #     faves_nums = int(match_re.group(1))
        # else:
        #     faves_nums = 0
        # comment_nums = response.css('a[href="#article-comment"] span::text').extract()[0]
        # match_re = re.match(".*?(\d+).*?", comment_nums)
        # if match_re:
        #     comment_nums = match_re.group(1)
        # else:
        #     comment_nums = 0
        # contens = response.css("div.entry").extract()
        # tag_list = response.css(".entry-meta-hide-on-mobile a::text").extract()
        # tag_list = ",".join(tag_list)
        #
        # article_item["url_object_id"] = get_ma5(response.url)
        # article_item["title"] = title
        # article_item["url"] = response.url
        # article_item["front_image_url"] = [front_image_url]
        # try:
        #     create_time = datetime.datetime.strptime(create_time, "%y/%m/%d").date()
        # except Exception as e:
        #     create_time = datetime.datetime.now().date()
        # article_item["create_time"] = create_time
        # article_item["faves_nums"] = faves_nums
        # article_item["tag_list"] = tag_list
        # article_item["contens"] = contens
        # article_item["comment_nums"] = comment_nums
        # article_item["praise_nums"] = praise_nums

        # 通过Itemloader加载item
        item_loader = ArticleItemLoader(item=JobboleArticleItem(), response=response)
        item_loader.add_css('title', '.entry-header h1::text')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_ma5(response.url))
        item_loader.add_value('front_image_url', [front_image_url])
        item_loader.add_css('create_time', '.entry-meta-hide-on-mobile::text')
        item_loader.add_css('faves_nums', 'span.bookmark-btn::text')
        item_loader.add_css('tag_list', '.entry-meta-hide-on-mobile a::text')
        item_loader.add_css('contens', 'div.entry')
        item_loader.add_css('comment_nums', 'a[href="#article-comment"] span::text')
        item_loader.add_css('praise_nums', 'span.vote-post-up h10::text')

        article_item = item_loader.load_item()
        yield article_item






