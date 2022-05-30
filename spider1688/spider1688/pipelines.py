# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from spider1688.spiders.al_category import AlCategorySpider
from itemadapter import ItemAdapter
import pymysql


class CategoryPipeline(object):
    def __init__(self):
        self.db = None
        self.cursor = None

    def open_spider(self, spider):
        if isinstance(spider, AlCategorySpider):
            # 建立数据库连接
            self.db = pymysql.connect(host='localhost',
                                      user='root',
                                      passwd='12345',
                                      port=3306,
                                      db='test',
                                      charset='utf8')
            self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        # 插入数据
        # self.cursor.execute('insert into test1(title,key2,) values(("%s"),("%s")) % (title[0],key2[0])')
        # results = (self.cursor.fetchall())
        # print(results)
        return item

    def close_spider(self, spider):
        # 关闭数据库连接
        if isinstance(spider, AlCategorySpider):
            # 游标对象断开连接
            self.cursor.close()

            # 数据库对象断开连接
            self.db.close()


