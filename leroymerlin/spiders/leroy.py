import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leroymerlin.items import LeroymerlinItem


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/keramogranit/pod-mramor']

    # def start_requests(self):
    #     for url in self.start_urls:
    #         return response(url=url, callback=self.parse,
    #                        headers={"User-Agent": "My UserAgent"},
    #                        meta={"proxy": "http://192.168.1.1:8050"})

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-qa='product-name']/@href").extract()
        next_page = self.start_urls[0] + response.xpath("//a[@data-qa-pagination-item='right']/@href").extract_first()
        print()
        for element in links:
            yield response.follow(element, callback=self.goods_parse)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def goods_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_xpath('title', "//h1[@slot='title']/text()")
        loader.add_xpath('prim_price', "//uc-pdp-price-view/meta[@itemprop='price']/@content")
        loader.add_xpath('photos', "//img[@itemprop='image' and @alt='product image']//@data-origin")
        loader.add_xpath('path', "//a//meta[@itemprop='name']/@content")
        loader.add_xpath('vcode', "//span[@slot='article']/@content")
        """specifications"""
        loader.add_xpath('spec_term', "//section[@class='pdp-section pdp-section--product-characteristicks']//div[@class='def-list__group']//dt//text()")
        loader.add_xpath('spec_def', "//section[@class='pdp-section pdp-section--product-characteristicks']//div[@class='def-list__group']//dd/text()")
        loader.add_value('link', response.url)
        yield loader.load_item()
