import scrapy

from euroCities.items import EuroCityItem

class EurSpider(scrapy.Spider):
    name = "euro"
    allowed_domains = ["wikipedia.org"]
    start_urls = [
                "http://en.wikipedia.org/wiki/Lists_of_cities_in_Europe"
            ]

    def parse(self, response):
        for sel in response.xpath("//ul/li"):
            item = EuroCityItem()
            item['title']=sel.xpath('a/text()').extract()
            item['link']=sel.xpath('a/@href').extract()
            item['desc']=None
            yield item
