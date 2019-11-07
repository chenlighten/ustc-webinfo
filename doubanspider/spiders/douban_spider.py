import scrapy
from doubanspider.items import DoubanspiderItem
from scrapy_redis.spiders import RedisSpider
import requests
from fake_useragent import UserAgent
import time



class DoubanSpider(RedisSpider):
    name = 'douban'
    custom_settings = {
        'ITEM_PIPELINES': {'doubanspider.pipelines.DoubanspiderPipeline': 300}
    }
    redis_key = 'myspider:start_urls' #从redis里面读url
    

    def parse(self, response):
        url = response.url
        if url.find('subject') != -1:
            yield self.process_music(response)

    
    def process_music(self, response):
        music_name = response.xpath('//*[@id="wrapper"]/h1/span/text()').extract_first()
        info = response.xpath('//*[@id="info"]')
        music_type = info.re_first(r'流派\S*\s*(..)')
        music_poster = response.xpath('//*[@id="mainpic"]/span/a/img/@src').get()
        
        item = DoubanspiderItem()
        item['music_name'] = music_name
        item['music_url'] = response.url
        item['music_type'] = music_type
        item['music_poster'] = [music_poster]

        short_remarks_list = []
        i = 1
        while True:
            if i > 5 or len(response.xpath('//*[@id="comments"]/ul/li[%i]'%i)) == 0:
                break
            short_remarks_dict = {}
            short_remarks_dict['id'] = \
                response.xpath('//*[@id="comments"]/ul/li[%i]/div/h3/span[2]/a/text()'%i).get()
            short_remarks_dict['content'] = \
                response.xpath('//*[@id="comments"]/ul/li[%i]/div/p/span/text()'%i).get()
            short_remarks_dict['star_number'] = \
                response.xpath('//*[@id="comments"]/ul/li[%i]/div/h3/span[2]/span[1]/@class'%i).re_first(r'allstar(.)')
            short_remarks_dict['useful_number'] = \
                response.xpath('//*[@id="comments"]/ul/li[%i]/div[@class="comment"]/h3[1]/span[1]/span[1]/text()'%1).get()
            short_remarks_list.append(short_remarks_dict)
            i += 1
        item['short_remarks'] = short_remarks_list

        long_remarks_list = []
        i = 1
        while True:
            if i > 3 or len(response.xpath('//div[@class="review-list  "]/div[%d]'%i)) == 0:
                break
            long_remarks_dict = {}
            long_remarks_dict['id'] = \
                response.xpath('//div[@class="review-list  "]/div[%d]//header[1]/a[2]/text()'%i).extract()
            long_remarks_dict['star_number'] = \
                response.xpath('//div[@class="review-list  "]/div[%d]//header[1]/span[1]/@class'%i).re_first(r'allstar(.)')
            long_remarks_dict['useful_number'] = \
                response.xpath('//div[@class="review-list  "]/div[%d]//a[@title="有用"]/span[1]/text()'%i).re_first(r'\s*([0-9]*)')
            content_url = response.xpath('//div[@class="review-list  "]/div[%d]//div[@class="main-bd"]/h2[1]/a[1]/@href'%i).get()
            long_remarks_dict['content'] = self.get_long_remark_content(content_url)
            long_remarks_list.append(long_remarks_dict)
            i += 1
        item['long_remarks'] = long_remarks_list

        with open('feiyunzhixia.html', 'wb') as f:
            f.write(response.body)

        return item

    
    def get_long_remark_content(self, url):
        time.sleep(0.2)
        response = requests.get(url, headers={'User-Agent': UserAgent().random})
        selector = scrapy.Selector(text=response.text)
        try:
            content_list = selector.xpath('//div[@class="review-content clearfix"]/p/text()').extract()
            content = content_list[0]
            for i in range(1, len(content_list)):
                content += content_list[i]
            with open('longremarkcontent.html', 'w') as f:
                f.write(response.text)
            return content
        except:
            try:
                content_list = selector.xpath('//div[@class="review-content clearfix"]/text()').extract()
                content = content_list[0]
                for i in range(1, len(content_list)):
                    content += content_list[i]
                with open('longremarkcontent.html', 'w') as f:
                    f.write(response.text)
                return content
            except:
                return "No long remark"

    
    def get_more_urls(self, response):
        music_urls = []
        for i in range(1, 26):
            music_url = \
                response.xpath('//*[@id="content"]/div/div[1]/div/table[%i]//a[1]/@href'%i).extract_first()
            music_urls.append(music_url)
        

        return music_urls
            