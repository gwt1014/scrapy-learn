# -*- coding: utf-8 -*-
import scrapy
import json
from jingdong.items import JingdongItem
import re
import requests


class JdSpider(scrapy.Spider):
    name = "jd"
    #allowed_domains = ["www.jd.com"]
    #start_urls = ['https://coll.jd.com/list.html?sub=23931&sort=sort_totalsales15_desc&stock=0&page=1']

    def start_requests(self):
        init_search = 'https://coll.jd.com/list.html?sub=23931&sort=sort_totalsales15_desc&stock=0&page='
        #init_search = 'https://list.jd.com/list.html?cat=9192,9197,12189&page='
        # target = {'行车记录仪': '23931'}  sub后面的代号
        maxpage = 1
        for i in range(1, maxpage + 1):
            yield scrapy.Request(url=init_search + str(i), callback=self.getitemList)
            # print(init_search+str(i))
            # print("#"*40)

    def getitemList(self, response):
        itemList = response.xpath(
            '//div[@id="plist"]/ul/li/div/div[@class="p-name"]/a/@href').extract()
        for itemUrl in itemList:
            #print('https:'+ itemUrl)
            yield scrapy.Request(url=('https:' + itemUrl), callback=self.getitemIdlist)

    def getitemIdlist(self, response):
        init_itemUrl = 'https://item.jd.com/{}.html'

        itemList = response.xpath(
            '//div[@id="choose-attrs"]/div//div[@class="dd"]/div/@data-sku').extract()
        for itemid in itemList:
            # print(init_itemUrl.format(itemid))
            yield scrapy.Request(url=init_itemUrl.format(itemid), callback=self.getitemInfo)
            # yield scrapy.Request(url = init_priceUrl.format(itemid),callback
            # = self.getitemPrice)

    # def getitemPrice(self,response):
    #     content = json.loads(response.text)
    #     item = JingdongItem()
    #     item['price'] = content[0]["op"]
    #     yield item
    #     # print(price)

    def getitemInfo(self, response):
        item = JingdongItem()

        init_priceUrl = 'https://p.3.cn/prices/mgets?skuIds=J_{}'
        itemid = re.findall('(\d+)', response.url)[0]

        try:
            item['title'] = "".join(response.xpath(
                '//div[@class="sku-name"]/text()').extract()).replace(' ', '').replace('\r', '').replace('\n', '')
            item['goods_url'] = response.url
            item['goods_id'] = itemid
            item['itemDetail'] = ";".join(response.xpath('//div[@class="p-parameter"]/ul[@class="parameter2 p-parameter-list"]/li/text()').extract())

            # yield item
            yield scrapy.Request(url=init_priceUrl.format(itemid), meta={'item': item}, callback=self.getitemPrice, dont_filter=True)
        except Exception as e:
            print('没有基础数据')

    def getitemPrice(self, response):
        init_commentUrl = 'https://sclub.jd.com/comment/productPageComments.action?productId={}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
        item = response.meta['item']
        try:
            content = json.loads(response.text)
        # print(content)
            item['price'] = content[0]["p"]
        # yield item
            yield scrapy.Request(url = init_commentUrl.format(item['goods_id']) , meta={'item': item}, callback=self.getitemComment, dont_filter=True)
        except Exception as e:
            print('没有价格数据')


    def getitemComment(self,response):
        item = response.meta['item']
        comment = json.loads(response.text)
        try:
            item['goodRate'] = comment['productCommentSummary']['goodRate']
            item['commentCount'] = comment['productCommentSummary']['commentCount']
            yield item

        except Exception as e:
            print('没有评论数据')

