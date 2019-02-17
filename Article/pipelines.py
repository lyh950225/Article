# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter
import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors



class ArticlePipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    #自定义JSON文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExportPipeline(object):
    #调用SCRAPY提供的Jsonexport 导出JSON文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ArticleImagePipelines(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                images_file_path = value["path"]
            item["front_image_path"] = images_file_path
            return item
            pass


class MysqlPipeline(object):
    # 自定义同步执行MYSQL插入
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'root', '12345', 'spiders', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole (title, url, create_time, faves_nums)
            VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item['title'], item['url'], item['create_time'], item['faves_nums']))
        self.conn.commit()


class MysqlTwistedPipline(object):
    # TWISTED异步插入MYSQL，只需要修改do_insert后面的逻辑即可重用
    # 根据不同的ITEM，构建不同的SQL语句并插入到MYDQL中
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
           host=settings["MYSQL_HOST"],
           db=settings["MYSQL_DBNAME"],
           user=settings["MYSQL_USER"],
           passwd=settings["MYSQL_PASSWORD"],
           charset='utf8',
           cursorclass=MySQLdb.cursors.DictCursor,
           use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用TWISTED将MYSQL插入异步执行
        query = self.dbpool.runinteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入异常
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)






