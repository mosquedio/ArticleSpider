# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#pipeline中主要是用来做数据存储的
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
import codecs
import json
import MySQLdb
import MySQLdb.cursors


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):       #要将settings中的pipeline设置打开
        return item


#采用twisted框架，对数据库进行异步插入
class MysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod                            #这里的写法不太看的懂,需要琢磨一下
    def from_settings(cls,settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
            )
        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)
        return cls(dbpool)

    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)               #处理异常

    #处理异步插入的异常
    def handle_error(self,failure):
        print(failure)

    #执行具体的插入
    def do_insert(self,cursor,item):
        insert_sql = """insert into  jobbole_article(title,url,url_object_id,create_date,fav_nums,content)values(%s,%s,%s,%s,%s,%s)"""
        cursor.execute(insert_sql, (item["title"], item["url"], item["url_object_id"], item["create_date"], item["fav_nums"], item["content"]))


#向mysql中保存数据(同步的)
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('192.168.176.128','root','root','scrapyspider',charset="utf8",use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """insert into  jobbole_article(title,url,url_object_id,create_date,fav_nums,content)values(%s,%s,%s,%s,%s,%s)"""
        self.cursor.execute(insert_sql,(item["title"],item["url"],item["url_object_id"],item["create_date"],item["fav_nums"],item["content"]))
        self.conn.commit()


#自定义json文件的导出
class JsonWithEncodingPipeline(object):
    def __init__(self):     #初始化的时候打开一个文件
        self.file = codecs.open('article.json','w',encoding="utf-8")
    def process_item(self, item, spider):
        lines = json.dumps(dict(item),ensure_ascii=False)+"\n"
        self.file.write(lines)
        return item
    def spider_closed(self,spider):             #在spider关闭的时候，将文件关闭
        self.file.close()


#调用scrapy提供的json export导出json文件(scrapy还提供了很多其他格式的文件导出,例如csv,xml)
class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open('articleexport.json','wb')
        self.exporter = JsonItemExporter(self.file,encoding="utf-8",ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

#基于ImagesPipeline创建的一个保存图片的Pipeline,将图片保存的路径也存放进了item中
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok,value in results:
                image_file_path = value["path"]
            item["front_img_path"] = image_file_path
        return item

