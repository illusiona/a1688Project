# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class MainspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Category(scrapy.Item):
    # 大类别名称
    b_category_name = scrapy.Field()
    b_category_url = scrapy.Field()
    # small category
    s_category_name = scrapy.Field()
    s_category_url = scrapy.Field()


class Product(scrapy.Item):
    company_name = scrapy.Field()              # 公司名
    company_city = scrapy.Field()              # city
    company_merchandise = scrapy.Field()       # 主营业产品
    company_address = scrapy.Field()           # 公司地址
    company_archive = scrapy.Field()           # 工厂档案
    company_turnover = scrapy.Field()          # 年交易额
    company_area = scrapy.Field()              # 公司面积
    company_staff = scrapy.Field()             # 员工总数
    company_device = scrapy.Field()            # 设备总数
    company_picture = scrapy.Field()           # 展示图片
    company_detail_picture = scrapy.Field()    # 详情图片
    company_service = scrapy.Field()           # 公司服务
    company_merch_url = scrapy.Field()         # 商品页url
    company_detail_url = scrapy.Field()        # 公司详情页url

    merch_name = scrapy.Field()                # 全部商品商品名
    merch_price = scrapy.Field()               # 全部商品价格
    merch_num = scrapy.Field()                 # 全部商品成交量

