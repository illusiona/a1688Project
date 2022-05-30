from spider1688.spiders import al_category
import scrapy
import json
from jsonpath import jsonpath


class JdProductSpider(scrapy.Spider):
    name = 'al_product'
    allowed_domains = ['1688.com']

    def start_url(self):
        pass

    def parse_product_base(self, response):
        # 解析详情页url并取出表头拼接全部商品url
        item = response.meta['item']
        print(response.text)
        result = json.loads(response.text)



