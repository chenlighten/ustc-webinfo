# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanspiderItem(scrapy.Item):
    # define the fields for your item here like:
    music_name = scrapy.Field()
    music_url = scrapy.Field()
    music_type = scrapy.Field()
    music_poster = scrapy.Field()
    
    

