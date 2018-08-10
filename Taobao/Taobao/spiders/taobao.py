# -*- coding: utf-8 -*-
import scrapy
from Taobao.items import TaobaoItem
from scrapy import Request
from Taobao.settings import DEFAULT_REQUEST_HEADERS
import re
import json



class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['taobao.com', 'tmall.com']
    start_urls = ['https://www.taobao.com/']



    def parse(self, response):
        target = '行车记录仪'
        maxpage = 2
        for i in range(0,maxpage):
            url = 'https://s.taobao.com/search?sort=sale-desc&q=' + str(target) + '&s=' + str(44*i)
            #print(url)
            yield Request(url=url,callback=self.getpageInfo)

    def getpageInfo(self,response):
        body = response.body.decode('utf-8')
        pattam_id = '"nid":"(.*?)"'
        id_list = re.compile(pattam_id).findall(body)
        #print(id_list)
        for i in range(0, len(id_list)):
            url = 'https://item.taobao.com/item.htm?id=' + str(id_list[i])
            yield Request(url=url, callback=self.next)

    def next(self, response):
        item = TaobaoItem()
        url = response.url
        pattam_url = 'https://(.*?).com'
        subdomain = re.compile(pattam_url).findall(url)
        #print(subdomain)
        if subdomain[0] != 'item.taobao':
            #天猫！！！
            title = response.xpath("//div[@class='tb-detail-hd']/h1/text()").extract()[0]
            pattam_price = '"defaultItemPrice":"(.*?)"'
            price = re.compile(pattam_price).findall(response.body.decode('utf-8', 'ignore')) # 天猫
            pattam_id = 'id=(.*?)&'
            itemID = re.compile(pattam_id).findall(url)[0]
            # salesVolume = response.xpath('//div[@class="tb-sell-counter"]/a/strong/text()').extract()[0]
            itemInfo = response.xpath('//div[@class="attributes"]/div/ul/li/text()').extract()
        else:
            #淘宝！！！
            title = response.xpath("//h3[@class='tb-main-title']/@data-title").extract()[0]
            price = response.xpath("//em[@class = 'tb-rmb-num']/text()").extract()[0] # 淘宝
            pattam_id = 'id=(.*?)$'
            itemID = re.compile(pattam_id).findall(url)[0]
            # salesVolume = response.xpath('//div[@class="tb-sell-counter"]/a/@title').extract()
            itemInfo = response.xpath('//div[@class="attributes"]/ul/li/text()').extract()
        #评论数太麻烦了，我有直接抓评论的方法，不理这个了
        # # 构造具有评论数量信息的包的网址
        # comment_url = 'https://dsr-rate.tmall.com/list_dsr_info.htm?itemId=' + str(itemID)
        # # 这个获取网址源代码的代码永远也不会出现错误，因为这个URL的问题，就算URL是错误的，也可以获取到对应错误网址的源代码。
        # # 所以不需要使用 try 和 except urllib.URLError as e 来包装。
        # comment_data = urllib.request.urlopen(comment_url).read().decode('utf-8', 'ignore')
        # pattam_comment = '"rateTotal":(.*?),"'
        # comment = re.compile(pattam_comment).findall(comment_data)
        

        item['title'] = title
        item['itemLink'] = response.url
        item['price'] = price
        item['itemID'] = itemID
        # item['salesVolume'] = salesVolume
        item['itemInfo'] = itemInfo
        yield item







#         # 名称
#     title = scrapy.Field()
# # 价格
#     price = scrapy.Field()
# # 月销量
#     salesVolume = scrapy.Field()
# # 评论数
#     comment = scrapy.Field()
# # 宝贝详情
#     itemInfo = scrapy.Field()
# # 链接
#     itemLink = scrapy.Field()
# # 宝贝ID
#     itemID = scrapy.Field()