import random

from selenium.webdriver.common.by import By
from ..items import Product
from scrapy.cmdline import execute
from selenium import webdriver
from lxml import etree
import pyautogui
import datetime
import scrapy
import time
import json
import re


class AlCategorySpider(scrapy.Spider):
    # debug
    name = "al_category"
    page_num = '2'
    # allowed_domains = ['1688.com']
    splicing = ''

    # start_urls = [r'https://search.1688.com/service/companyInfoSearchDataService?keywords=%C8%C6%CF%DF%BB%FA&spm='
    #               f'a26352.13672862.searchbox.input&%27f%27beginPage={page_num}&province=%E5%B9%BF%E4%B8%9C&async=false&a'
    #               r'syncCount=6&pageSize=20&pageName=findPCFactory&_bx-v=1.1.20']

    def start_requests(self):
        start_url_list = []
        for i in range(1, 30):
            start_url_list.append(r'https://search.1688.com/service/companyInfoSearchDataService?keywords='
                                  f'%C8%C6%CF%DF%BB%FA&spm=a26352.13672862.searchbox.input&%27f%27beginPage={i}&p'
                                  r'rovince=%E5%B9%BF%E4%B8%9C&async=false&asyncCount=6&pageSize=20&pageName=findPCFactory&_bx-v=1.1.20')

        for i in range(0, 29):
            time.sleep(1)
            yield scrapy.Request(start_url_list[i], callback=self.parse, dont_filter=True)


    def parse(self, response):
        # print(response.body.decode('utf-8'))
        result = json.loads(response.body.decode('utf-8'))
        datas = result['data']['data']['companyWithOfferLists']
        # 遍历列表
        for data in datas:
            item = Product()

            item.fields['company_name'] = data['factoryInfo']['company']

            item.fields['company_city'] = data['factoryInfo']['city']

            item.fields['company_detail_url'] = data['factoryInfo']['factoryDetailUrl']

            item.fields['company_detail_picture'] = data['factoryInfo']['picUrl']

            item.fields['company_service'] = data['factoryInfo']['productionService']

            # 拼接全部商品页面url   可通过请求items.fields['company_picture']中进旺拼接得到

            lis_num = 0
            item = Product()
            item.fields['company_picture'] = data['factoryOfferList'][lis_num]['picUrl']

            item.fields['company_merchandise'] = data['factoryOfferList'][lis_num]['simpleSubject']

            lis_num += 1
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

        f_merch_url = re.split('[/.]', html.xpath('//*[@class="actionItem"]/@href')[0])[2]
        item['company_merch_url'] = f'https://{f_merch_url}.1688.com/page/offerlist.htm?spm=0.0.wp_pc_common_topnav_38229151.0'
        yield scrapy.Request(item['company_merch_url'], callback=self.parse_all_merch, meta={'item': item})

    def parse_all_merch(self, response):
        item = response.meta['item']
        # 解析商页url 并拼接
        # 初始化浏览器并配置参数开始无痕模式
        option = webdriver.ChromeOptions()
        option.add_argument('--incognito')
        driver = webdriver.Chrome(options=option)
        driver.maximize_window()
        driver.get(item["company_merch_url"])
        merch_name = []
        merch_num = []
        merch_price = []
        time.sleep(random.randint(4, 6))
        while True:
            try:
                j = 0  # 判断有多少个价格拆分的数据  随着翻页重置
                for i in range(30):     # 30个商品，部分无推荐
                    try:
                        merch_name.append(driver.find_elements(by=By.XPATH, value='//*/div/p[@title]')[i].text)
                        item['merch_name'] = merch_name
                        merch_num.append(driver.find_elements(by=By.XPATH, value='//*[@title="累计销量"]')[i].text)
                        item['merch_num'] = merch_num
                        # 自带万 二级框带万 二级框只有小数点
                        price = driver.find_elements(by=By.XPATH, value='//*[@style="position: relative; box-sizing: border-box; flex-direction: column; align-content: flex-start; flex-shrink: 0; margin-top: 0px; margin-bottom: 0px; color: rgb(255, 41, 0); font-size: 24px; line-height: 24px; font-weight: bold;"]')[i].text
                        try:
                            price_sec = driver.find_elements(by=By.XPATH, value='//*[@style="position: relative; box-sizing: border-box; flex-direction: column; '
                                                                                'align-content: flex-start; flex-shrink: 0; margin-top: 0px; margin-bottom: 0px; '
                                                                                'color: rgb(255, 41, 0); font-size: 24px; line-height: 24px; font-weight: bold;"]'
                                                                                '/following-sibling::span')[j].text
                            j += 1
                            merch_price.append(price + price_sec)
                            # 如果一级索引自带万字，则回滚二级框索引下表并pop list，再直接填入一级框内的内容
                            if price[-1] == '万':
                                j -= 1
                                merch_price.pop()
                                merch_price.append(price)

                        except:
                            merch_price.append(price)

                        item['merch_price'] = merch_price

                    except:
                        break

                # 如果下一页的RGB值小于255，则当前页为最后一页
                if int(driver.find_element(by=By.XPATH, value='//*/button[contains(@style,background)][2]').get_attribute('style')[16:19]) < 255:
                    break

                # 判断是否有下一页
                driver.find_element(by=By.XPATH, value='//*/button[contains(@style,background)][2]').click()

                # 留缓冲数据的时间
                time.sleep(2)
            except:
                break
        print(item)
        driver.close()
        yield item







