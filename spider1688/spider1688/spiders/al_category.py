
from spider1688.items import Product
from scrapy.cmdline import execute
from lxml import etree
import datetime
import scrapy
import json
import re


class AlCategorySpider(scrapy.Spider):
    # debug
    name = "al_category"
    page_num = '2'
    allowed_domains = ['1688.com']
    # 滑动加载数据
    start_urls = [r'https://search.1688.com/service/companyInfoSearchDataService?keywords=%C8%C6%CF%DF%BB%FA&hideMainTab=1&spm=a26352.13672862.searchbox.input&'
                  f'beginPage={page_num}&province=%E5%B9%BF%E4%B8%9C&async=true&asyncCount=6&pageSize=20&requestId=faztmSHPEtXRyGetejiSh2jE4fse6wFthYyJiDWnYmwKPzCW&sessionId=b83181af63e948879cdc5419ddfc73c0&startIndex=0&pageName=findPCFactory&_bx-v=1.1.20']
    splicing = ''
    def parse(self, response):
        # print(response.body.decode('utf-8'))
        result = json.loads(response.body.decode('utf-8'))
        datas = result['data']['data']['companyWithOfferLists']
        # 遍历列表
        for data in datas:
            item = Product()
            # 大分类信息
            item.fields['company_name'] = data['factoryInfo']['company']

            item.fields['company_city'] = data['factoryInfo']['city']

            item.fields['company_detail_url'] = data['factoryInfo']['factoryDetailUrl']

            item.fields['company_detail_picture'] = data['factoryInfo']['picUrl']
            # pic_url.append(data['factoryInfo']['picUrl'])
            item.fields['company_service'] = data['factoryInfo']['productionService']

            # 拼接全部商品页面url   可通过请求items.fields['company_picture']中进旺拼接得到
            # items.fields['company_merch_url'] = data['']

            lis_num = 0
            item = Product()
            item.fields['company_picture'] = data['factoryOfferList'][lis_num]['picUrl']

            item.fields['company_merchandise'] = data['factoryOfferList'][lis_num]['simpleSubject']

            lis_num += 1
            print(item.fields)
            yield item
            yield scrapy.Request(item.fields['company_detail_url'], callback=self.detail_page, meta={'item': item})

        # vis detail page
    def detail_page(self, response):
        item = response.meta['item'].fields
        # 发起详情页req
        scrapy.Request(response.meta['item'].fields['company_detail_url'])
        html = etree.HTML(response.text)
        try:
            item['company_archive'] = html.xpath('//*[@class="com_info_all"]')[0].text
        except:
            item['company_archive'] = ''
        try:
            item['company_address'] = html.xpath('//*[@class="location"]')[0].text
        except:
            item['company_address'] = ''

        # 匹配出的时间为当前时间则没有该条数据并置空
        pattern_est = re.compile(r"(\d{4}-\d{1,2}-\d{1,2})")
        est_time = pattern_est.findall(response.text)
        try:
            if est_time[-2] != str(datetime.datetime.now())[:10]:
                item['company_est_time'] = est_time[-2]
            else:
                item['company_est_time'] = ''
        except:
            pass

        # 第一个即为年交易额
        pattern_turn = re.compile(r"(\d+\u4e07)")
        turnover = pattern_turn.findall(response.text)
        try:
            item['company_turnover'] = turnover[0]
        except:
            item['company_turnover'] = ''

        pattern_area = re.compile(r"(\d+\u5e73\u65b9)")
        area = pattern_area.findall(response.text)
        try:
            item['company_area'] = area[0]
        except:
            item['company_area'] = ''

        pattern_staff = re.compile(r"(\d+\u4eba)")
        staff = pattern_staff.findall(response.text)
        try:
            item['company_staff'] = staff[0]
        except:
            item['company_staff'] = ''

        pattern_device = re.compile(r"(\d+\u53f0)")
        device = pattern_device.findall(response.text)
        try:
            item['company_device'] = device[0]
        except:
            item['company_device'] = ''

        # 拼接全部商品页url

        f_merch_url = re.split('[//.]',html.xpath('//*[@class="actionItem"]/@href')[0])[2]
        item['company_merch_url'] = f'https://{f_merch_url}.1688.com/page/offerlist.htm?spm=0.0.wp_pc_common_topnav_38229151.0'

        yield scrapy.Request(item['company_merch_url'], callback=self.parse_all_merch, meta={'item': item})

    def parse_all_merch(self, response):
        item = response.meta['item']
        # 解析商页url 并拼接

        mer_id = ''
        all_url = f'https://detail.1688.com/offer/{mer_id}.html?spm=a2615.7691456.wp_pc_common_offerlist_45753076.0'

        item['company_all_merch_url'] = ''





