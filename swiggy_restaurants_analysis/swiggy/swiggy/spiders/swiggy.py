import scrapy


class SwiggySpider(scrapy.Spider):
    name = "swiggy"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def parse(self, response):
        pass
