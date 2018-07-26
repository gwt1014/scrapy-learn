# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
   
    baseURL = "https://hr.tencent.com/position.php?start="
    offset = 0
    start_urls = [baseURL + str(offset)]



    def parse(self, response):
        
        node_list = response.xpath("//tr[@class='odd'] | //tr[@class='even']")

        for node in node_list:
            item = TencentItem()
            #职位名称
            item['positionName'] = node.xpath('./td[1]/a/text()').extract()[0]
            # 职位链接
            item['positionLink'] = "https://hr.tencent.com/" + node.xpath('./td[1]/a/@href').extract()[0]
            # 职位类型
            if len(node.xpath('./td[2]/text()')):
                item['positonType'] = node.xpath('./td[2]/text()').extract()[0]
            else:
                item['positonType'] = ""
            # 招聘人数
            item['peopleNumber'] = node.xpath('./td[3]/text()').extract()[0]
            # 工作地点
            item['workLocation'] = node.xpath('./td[4]/text()').extract()[0]
            # 发布时间
            item['poblishTime'] = node.xpath('./td[5]/text()').extract()[0]

            yield item
        # 这是拼接URL的方法，对于读取json的时候，因为没有原始的url随意用构建
        # 这里也有问题如果 如果职位数变了，就不是3600了，每次都得改。

        # if self.offset < 50:
        #     self.offset += 10
        #     url = self.baseURL + str(self.offset)
        #     yield scrapy.Request(url, callback = self.parse)

        # 方法二，用下一页来做，这样就不管多少职位都能搞了
        if len(response.xpath('//a[@class="noactive" and @id="next"]')) == 0:
            url = response.xpath('//a[@id="next"]/@href').extract()[0]
            yield scrapy.Request('https://hr.tencent.com/' + url, callback = self.parse)