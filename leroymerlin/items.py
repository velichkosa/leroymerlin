# Define here the models for your scraped items

# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from itemloaders.processors import MapCompose, TakeFirst
import scrapy


class LeroymerlinItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    prim_price = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    path = scrapy.Field()
    vcode = scrapy.Field(output_processor=TakeFirst())
    spec_term = scrapy.Field()
    spec_def = scrapy.Field()
    specifications = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field()
    print()
    pass
