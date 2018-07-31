# -*- coding: utf-8 -*-
import scrapy
from ziru.items import ZiruItem
import re

class ZiruSpider(scrapy.Spider):
    name = 'Ziru'
    allowed_domains = ['ziroom.com']
    start_urls = ['http://www.ziroom.com/z/nl/z3.html']

    def parse(self, response):
        blockUrl_list = response.xpath(
            '//dl[@class="clearfix zIndex6"]/dd/ul/li/div/span/a/@href').extract()
        for blockUrl in blockUrl_list:
            yield scrapy.Request("http:" + blockUrl, callback = self.parse_gethouseUlr)
            #print("http:" + blockUrl)

    def parse_gethouseUlr(self, response):
        houseUrl_list = response.xpath(
            '//ul/li[@class="clearfix"]/div/h3/a/@href').extract()
        for houseUrl in houseUrl_list:
            #print("http:" + houseUrl)
            yield scrapy.Request("http:" + houseUrl, callback=self.parse_getHouseInfo)

        next_page = response.xpath(
            '//div[@class="pages"]/a[@class="next"]/@href').extract()
        if len(next_page):
            # print("有下一页")
            # print("http:" + next_page[0])
            yield scrapy.Request("http:" + next_page[0], callback=self.parse_gethouseUlr)

        # else :
        #     print("啥也没有")

    def parse_getHouseInfo(self, response):
        #print("##**"*40)

        item = ZiruItem()
        item['houseID'] = response.xpath('//div[@class="aboutRoom gray-6"]/h3/text()').extract()[0]
        item['name'] = response.xpath('//div[@class="room_name"]/h2/text()').extract()[0]
        # item['houseType'] = "??"
        item['district'] = re.findall('\[(.*?) (.*?)\]',response.xpath('//div[@class="room_name"]/p/span[1]/text()').extract()[0].replace('\n',''),re.S)[0][0]
        item['region'] = re.findall('\[(.*?) (.*?)\]',response.xpath('//div[@class="room_name"]/p/span[1]/text()').extract()[0].replace('\n',''),re.S)[0][1].replace(' ','')
        if len(re.findall('(\d+\.\d+)',response.xpath('//ul[@class="detail_room"]/li[1]/text()').extract()[0],re.S)):
            item['area'] = re.findall('(\d+\.\d+)',response.xpath('//ul[@class="detail_room"]/li[1]/text()').extract()[0],re.S)[0]
        else:
            item['area'] = re.findall('(\d+)',response.xpath('//ul[@class="detail_room"]/li[1]/text()').extract()[0],re.S)[0]
        item['direction'] = response.xpath('//ul[@class="detail_room"]/li[2]/text()').extract()[0].replace('朝向： ','')
        item['house_type'] = response.xpath('//ul[@class="detail_room"]/li[3]/text()').extract()[0].replace('户型： ','')
        # item['price'] = response.xpath('//div[@class="aboutRoom gray-6"]/h3/text()').extract()[0]
        # item['price_type'] = response.xpath('//div[@class="aboutRoom gray-6"]/h3/text()').extract()[0]
        item['floor'] = response.xpath('//ul[@class="detail_room"]/li[4]/text()').extract()[0].replace('楼层： ','')
        #item['subway1'] = subway1 = response.xpath('//span[@class="lineList"]/text()').extract()[0].replace('\n','').replace(' ','')


        # item['house_url'] = response.xpath('//div[@class="aboutRoom gray-6"]/h3/text()').extract()[0]
        
        # laji = response.xpath('//div[@class="room_name"]/p/span[1]/text()').extract()[0].replace('\n','')
        # district = re.findall('\[(.*?) (.*?)\]',response.xpath('//div[@class="room_name"]/p/span[1]/text()').extract()[0].replace('\n',''),re.S)[0][0]
        # region = re.findall('\[(.*?) (.*?)\]',response.xpath('//div[@class="room_name"]/p/span[1]/text()').extract()[0].replace('\n',''),re.S)[0][1].replace(' ','')
        # if len(re.findall('(\d+\.\d+)',response.xpath('//ul[@class="detail_room"]/li[1]/text()').extract()[0],re.S)):
        #     area = re.findall('(\d+\.\d+)',response.xpath('//ul[@class="detail_room"]/li[1]/text()').extract()[0],re.S)[0]
        # else:
        #     area = re.findall('(\d+)',response.xpath('//ul[@class="detail_room"]/li[1]/text()').extract()[0],re.S)[0]
        # # #print(district)
        # print(area)
        # url = response.xpath('//li[@id="ziroom_login"]/a/@href').extract()[0]
        # #url = re.findall('=(.*?)',response.xpath('//li[@id="ziroom_login"]/a/@href').extract()[0],re.S)
        # print(url)