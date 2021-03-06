import scrapy
from doubanspider.items import MusicUrlItem
import requests
from fake_useragent import UserAgent
import time



class DoubanSpider(scrapy.Spider):
    name = 'allmusic'
    custom_settings = {
        'ITEM_PIPELINES': {'doubanspider.pipelines.AllMusicPipeline': 300}
    }

    def start_requests(self):
        # urls = ['https://music.douban.com/top250?start=%d'%(i*25) for i in range(10)]
        urls = ['https://music.douban.com/subject/25927970/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    
    def parse(self, response):
        url = response.url
        if url.find('subject') != -1:
            item = MusicUrlItem()
            item['url'] = url
            yield item
            more_urls = self.parse_music_page(response)
            for more_url in more_urls:
                yield scrapy.Request(more_url, self.parse)
    

    def parse_music_page(self, response):
        more_urls = []
        for i in range(1, 11):
            more_url = response.xpath('//*[@id="db-rec-section"]/div/dl[%d]/dd/a/@href'%i).get()
            if more_url is not None:
                more_urls.append(more_url)
        return more_urls