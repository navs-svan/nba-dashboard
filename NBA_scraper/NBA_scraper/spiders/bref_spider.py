import scrapy


class BrefSpiderSpider(scrapy.Spider):
    name = "bref_spider"
    allowed_domains = ["basketball-reference.com"]
    start_urls = ["https://basketball-reference.com"]

    def parse(self, response):
        pass
