# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaSecondhandItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    total_price = scrapy.Field()
    unit_price = scrapy.Field()
    area = scrapy.Field()
    b_type = scrapy.Field()
    configuration = scrapy.Field()
    renovation = scrapy.Field()
    floor = scrapy.Field()
    orientation = scrapy.Field()
    location = scrapy.Field()
    info = scrapy.Field()
    