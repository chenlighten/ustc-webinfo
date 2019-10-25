import scrapy

class DoubanSpider(scrapy.Spider):
    name = 'douban'

    def start_requests(self):
        urls = [
            'https://music.douban.com/subject/30204901/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        filename = 'feiyunzhixia.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s'%filename)