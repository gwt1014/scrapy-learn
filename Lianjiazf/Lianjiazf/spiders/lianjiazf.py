# -*- coding: utf-8 -*-
import scrapy
from Lianjiazf.items import LianjiazfItem
import json

class LianjaizfSpider(scrapy.Spider):
    name = 'lianjiazf'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://bj.lianjia.com/zufang/']

    def parse(self, response):
        # 获取每个城区的url，去掉燕郊和香河
        district_list = response.xpath(
            '//*[@id="filter-options"]/dl[1]/dd/div/a/@href').extract()[1:-2]
        for district in district_list:
            yield scrapy.Request('https://bj.lianjia.com' + district, callback=self.parse_gethouseUrl)
            #print('http://bj.lianjia.com' + district)
            # print('#'*40)

    # def parse_getblockUrl(self, response):
    #     # 获取每个地区的url
    #     block_list = response.xpath(
    #         '//*[@id="filter-options"]/dl[1]/dd/div[2]/a/@href').extract()
    #     for block in block_list:
    #         # url里加"ng1nb1/"是为了不看车库和地下室
    #         yield scrapy.Request('https://bj.lianjia.com' + block, callback=self.parse_gethouseUrl)
    #         # print('http://bj.lianjia.com' + blockUrl)
    #         # print('#'*40)

    def parse_gethouseUrl(self, response):
        # 获取每个地区的二手房的URL
        houseUrl_list = response.xpath(
            '//*[@id="house-lst"]/li/div[2]/h2/a/@href').extract()
        for house in houseUrl_list:
            # print(house)
            # print('#'*40)
            yield scrapy.Request(house, callback=self.parse_gethouseInfo)

        ################################################################
        #########翻页还没弄##############################################
        ################################################################
        # # 下一页
        # # 每个页面进去以后 都有当前页和总页数，根据这个进行判断
        totalPage = json.loads(response.xpath(
            '//div[@class="list-wrap"]/div[2]/@page-data').extract()[0])["totalPage"]
        curPage = json.loads(response.xpath(
            '//div[@class="list-wrap"]/div[2]/@page-data').extract()[0])["curPage"]
        if curPage < totalPage:
            next_page = curPage + 1
            url = 'http://bj.lianjia.com' + \
                response.xpath('//div[@class="list-wrap"]/div[2]/@page-url').extract()[
                    0].replace("{page}", str(next_page))
            yield scrapy.Request(url, callback=self.parse_gethouseUrl)

    def parse_gethouseInfo(self, response):
        # 在房屋页面获取各种信息
        item = LianjiazfItem()


        item['houseID'] = response.xpath(
            '/html/body/div[4]/div[2]/div[2]/div[4]/span/text()').extract()[0].lstrip('链家编号：')
        item['title'] = response.xpath(
            '/html/body/div[4]/div[1]/div/div[1]/h1/text()').extract()[0]
        item['district'] = response.xpath(
            '/html/body/div[4]/div[2]/div[2]/div[2]/p[7]/a[1]/text()').extract()[0]
        item['block']= response.xpath(
            '/html/body/div[4]/div[2]/div[2]/div[2]/p[7]/a[2]/text()').extract()[0]
        item['communityName'] = response.xpath(
            '/html/body/div[4]/div[2]/div[2]/div[2]/p[6]/a[1]/text()').extract()[0]
        item['houseLink'] = 'https://bj.lianjia.com/zufang/' + item['houseID'] + '.html'
        item['roommainInfo'] = response.xpath(
            '/html/body/div[4]/div[2]/div[2]/div[2]/p[2]/text()').extract()[0]
        item['floor'] = response.xpath(
            '/html/body/div[4]/div[2]/div[2]/div[2]/p[3]/text()').extract()[0]
        item['orientation'] = response.xpath(
            '/html/body/div[4]/div[2]/div[2]/div[2]/p[4]/text()').extract()[0]
        item['builtArea'] = response.xpath(
            '/html/body/div[4]/div[2]/div[2]/div[2]/p[1]/text()').extract()[0].rstrip('平米')
        item['subway'] = response.xpath(
            '/html/body/div[4]/div[2]/div[2]/div[2]/p[5]/text()').extract()[0]
        item['heatingMode'] = response.xpath(
            '//*[@id="introduction"]/div/div[2]/div[1]/div[2]/ul/li[4]/text()').extract()[0]
        item['houseState'] = response.xpath(
            '//*[@id="introduction"]/div/div[2]/div[1]/div[2]/ul/li[3]/text()').extract()[0]
        yield item
