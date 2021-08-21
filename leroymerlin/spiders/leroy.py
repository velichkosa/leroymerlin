import scrapy


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['http://leroymerlin.ru/']

    def parse(self, response):
        pass
