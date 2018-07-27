# -*- coding: utf-8 -*-
import scrapy
import json
from Lianjia2sf.items import Lianjia2SfItem


class Lianjia2sfSpider(scrapy.Spider):
    name = 'lianjia2sf'
    allowed_domains = ['bj.lianjia.com']
    start_urls = ['http://bj.lianjia.com/ershoufang/']

    def parse(self, response):
        # 获取每个城区的url，去掉燕郊和香河
        district_list = response.xpath(
            '//div[@class="sub_nav section_sub_nav"]/a/@href').extract()[:-2]
        for district in district_list:
            yield scrapy.Request('http://bj.lianjia.com' + district, callback=self.parse_getblockUrl)
            # print('http://bj.lianjia.com' + districtUrl)
            # print('#'*40)

    def parse_getblockUrl(self, response):
        # 获取每个地区的url
        block_list = response.xpath(
            '//div[@class="sub_sub_nav section_sub_sub_nav"]/a/@href').extract()
        for block in block_list:
            #url里加"ng1nb1/"是为了不看车库和地下室
            yield scrapy.Request('http://bj.lianjia.com' + block + "ng1nb1/", callback=self.parse_gethouseUrl)
            # print('http://bj.lianjia.com' + blockUrl)
            # print('#'*40)

    def parse_gethouseUrl(self, response):
        #获取每个地区的二手房的URL
        houseUrl_list = response.xpath(
            '//li[@class="clear LOGCLICKDATA"]/a/@href').extract()
        for house in houseUrl_list:
            # print(house)
            # print('#'*40)
            yield scrapy.Request(house, callback=self.parse_gethouseInfo)

        # 下一页
        # 每个页面进去以后 都有当前页和总页数，根据这个进行判断
        totalPage = json.loads(response.xpath(
            '//div[@class="page-box house-lst-page-box"]/@page-data').extract()[0])["totalPage"]
        curPage = json.loads(response.xpath(
            '//div[@class="page-box house-lst-page-box"]/@page-data').extract()[0])["curPage"]
        if curPage < totalPage:
            next_page = curPage + 1
            url = 'http://bj.lianjia.com' + \
                response.xpath('//div[@class="page-box house-lst-page-box"]/@page-url').extract()[
                    0].replace("{page}", str(next_page))
            yield scrapy.Request(url, callback=self.parse_gethouseUrl)

    def parse_gethouseInfo(self, response):
        #在二手房页面获取各种信息

        item = Lianjia2SfItem()

        # 基本信息
        item['houseID'] = response.xpath(
            '//div[@class="houseRecord"]/span[@class="info"]/text()').extract()[0]
        item['title'] = response.xpath(
            '//div[@class="title"]/h1/text()').extract()[0]
        item['district'] = response.xpath(
            '//span[@class="info"]/a[1]/text()').extract()[0]
        item['block'] = response.xpath(
            '//span[@class="info"]/a[2]/text()').extract()[0]
        item['communityName'] = response.xpath(
            '/html/body/div[5]/div[2]/div[4]/div[1]/a[1]/text()').extract()[0]
        item['totlePrice'] = response.xpath(
            '//span[@class="total"]/text()').extract()[0]
        item['unitPrice'] = response.xpath(
            '//span[@class="unitPriceValue"]/text()').extract()[0]
        item['houseLink'] = response.xpath(
            '//head/link[@rel="canonical"]/@href').extract()[0]
        #下面的房屋详细信息
        item['roommainInfo'] = response.xpath(
            '//div[@class="base"]/div[@class="content"]/ul/li[1]/text()').extract()[0]
        item['floor'] = response.xpath(
            '//div[@class="base"]/div[@class="content"]/ul/li[2]/text()').extract()[0]
        item['builtArea'] = response.xpath(
            '//div[@class="base"]/div[@class="content"]/ul/li[3]/text()').extract()[0]
        item['roomType'] = response.xpath(
            '//div[@class="base"]/div[@class="content"]/ul/li[4]/text()').extract()[0]
        item['useArea'] = response.xpath(
            '//div[@class="base"]/div[@class="content"]/ul/li[5]/text()').extract()[0]
        item['builtType'] = response.xpath(
            '//div[@class="base"]/div[@class="content"]/ul/li[6]/text()').extract()[0]
        item['orientation'] = response.xpath(
            '//div[@class="base"]/div[@class="content"]/ul/li[7]/text()').extract()[0]
        item['built'] = response.xpath(
            '//div[@class="base"]/div[@class="content"]/ul/li[8]/text()').extract()[0]
        item['decoration'] = response.xpath(
            '//div[@class="base"]/div[@class="content"]/ul/li[9]/text()').extract()[0]
        item['liftType'] = response.xpath(
            '//div[@class="base"]/div[@class="content"]/ul/li[10]/text()').extract()[0]
        item['heatingMode'] = response.xpath(
            '///div[@class="base"]/div[@class="content"]/ul/li[11]/text()').extract()[0]
        item['lift'] = response.xpath(
            '//div[@class="base"]/div[@class="content"]/ul/li[12]/text()').extract()[0]
        item['propertyRights'] = response.xpath(
            '//div[@class="base"]/div[@class="content"]/ul/li[13]/text()').extract()[0]
        #房屋交易信息
        item['houseType'] = response.xpath(
            '//div[@class="transaction"]/div[@class="content"]/ul/li[4]/span[2]/text()').extract()[0]
        #返回item给pipelines进行数据存储
        yield item
