import scrapy
from doubanspider.items import DoubanspiderItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'

    def start_requests(self):
        urls = [
            'https://douban.com/subject/30204901/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        music_name = response.xpath('//*[@id="wrapper"]/h1/span/text()').extract_first()
        
        item = DoubanspiderItem()
        item['music_name'] = music_name
        with open('feiyunzhixia.html', 'wb') as f:
            f.write(response.body)