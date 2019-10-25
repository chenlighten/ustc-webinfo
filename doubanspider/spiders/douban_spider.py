import scrapy
from doubanspider.items import DoubanspiderItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    start_urls = ['https://music.douban.com/subject/30204901/']
    
    def parse(self, response):
        music_name = response.xpath('//*[@id="wrapper"]/h1/span/text()').extract_first()
        
        item = DoubanspiderItem()
        item['music_name'] = music_name
        