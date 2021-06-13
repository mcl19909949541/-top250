import scrapy
from Douban250.items import Douban250Item
import re

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        item = Douban250Item()
        for node in response.xpath('//ol[@class="grid_view"]/li'):

            #电影名
            item['name'] = node.xpath('.//span[@class="title"][1]/text()').extract()[0]
            #电影评分
            item['score'] = node.xpath('.//div[@class="star"]/span[2]/text()').extract()[0]
            #电影评语
            item['quote'] = node.xpath('.//p[@class="quote"]/span/text()').extract_first()#有一项没有quote所以用first
            #图片地址
            item['cover_url'] = node.xpath('.//div[@class="pic"]/a/img/@src').extract()[0]
            # 导演
            findBd = re.compile(r'导演(.*?)\xa0', re.S)
            director = ''.join(node.xpath('.//div[@class="bd"]/p/text()').extract()[0]).strip() + '\n' + ''.join(node.xpath('.//div[@class="bd"]/p[1]/text()').extract()[1]).strip()
            item['introduce'] = bd = re.findall(findBd, director)

            print(item)  # 看看输出
            yield item

           #








        next_page = response.xpath('//span[@class="next"]/a/@href')
        if next_page:
            url = 'https://movie.douban.com/top250' + next_page[0].extract()
            yield scrapy.Request(url, callback=self.parse)

