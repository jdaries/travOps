import scrapy

from euroCities.items import CityListItem, CityLinkItem, CityItem
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor

class EurSpider(CrawlSpider):
    name = "euro"
    allowed_domains = ["wikipedia.org"]
    start_urls = [
                "http://en.wikipedia.org/wiki/Lists_of_cities_in_Europe"
            ]
    rules = [Rule(LxmlLinkExtractor(allow=("http://en.wikipedia.org/wiki/List_of_cities",),restrict_xpaths="//ul/li"), callback="parse_item", follow=True)]

    def parse(self, response):
        for sel in response.xpath("//ul/li"):
            item = CityListItem()
            item['title']=sel.xpath('a/text()').extract()
            item['link']=sel.xpath('a/@href').extract()
            request = scrapy.Request(url="http://en.wikipedia.org"+item['link'][0], callback=self.scrape_cities)
            try:
                request.meta['country'] = item['link'][0].split("_")[-1]
            except:
                request.meta['country'] = None
            yield request

    def scrape_cities(self,response2):
        for sel2 in response2.xpath("//ul/li"):
            item = CityLinkItem()
            item['title']=sel2.xpath('a/text()').extract()
            item['link']=sel2.xpath('a/@href').extract()
            request = scrapy.Request(url="http://en.wikipedia.org"+item['link'][0], callback=self.scrape_locations)
            request.meta['city'] = item['title']
            request.meta['country'] = response2.meta['country']
            yield request

    def scrape_locations(self,response3):
        item = CityItem()
        for sel3 in response3.xpath("//span[contains(@class,'latitude')]"):
            item['city'] = response3.meta['city']
            item['country'] = response3.meta['country']
            item['latitude'] = sel3.xpath("text()").extract()
        for sel4 in response3.xpath("//span[contains(@class, 'longitude')]"):
            item['longitude'] = sel4.xpath("text()").extract()
        if item.get('latitude') and item.get('country'):
            yield item
        else:
            pass
