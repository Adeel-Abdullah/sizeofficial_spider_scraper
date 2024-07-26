import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SizeofficialSpider(CrawlSpider):
    name = "sizeofficial"
    allowed_domains = ["sizeofficial.es"]
    start_urls = ["https://www.sizeofficial.es"]
    count = 0
    max_count = 50

    rules = (Rule(LinkExtractor(allow=r"product/"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        if self.count >= self.max_count:
            return
        self.count += 1
        item = {}
        item["url"] = response.url
        item["title"] = response.xpath('//div[@id="productItemTitle"]/h1/text()').get()
        item["price"] = response.css('.itemPrices > span::text').get()
        item["start-url"] = response.xpath('//span[@class="active"]//preceding-sibling::span[@class="no"]//@href').getall()[-1]
        item["sizes"] = response.xpath('//div[@id="productSizeStock"]/button/text()').getall()
        yield {
            "name": item["title"],
            "link": item["url"],
            "price": item["price"],
            "start-url": item["start-url"],
            "sizes": [i for i in item["sizes"] if i.strip()],   
        }
