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
        info = response.xpath('//*[@id="info"]')
        music_type = info.re_first(r'流派\S*\s*(..)')
        music_poster = response.xpath('//*[@id="mainpic"]/span/a/img/@src').get()
        
        item = DoubanspiderItem()
        item['music_name'] = music_name
        item['music_url'] = response.url
        item['music_type'] = music_type
        item['music_poster'] = [music_poster]
# //*[@id="comments"]/ul/li[1]/div/h3/span[2]/a
# //*[@id="comments"]/ul/li[2]/div/h3/span[2]/a
        short_remarks_list = []
        for i in range(1, 6):
            short_remark = response.xpath('//*[@id="comments"]//li[{:d}]'.format(i))
            short_remarks_dict = {}
            short_remarks_dict['id'] = short_remark.xpath('//div/h3/span[2]/a/text()').extract_first()
            short_remarks_dict['content'] = short_remark.xpath('//div/p/span/text()').extract_first()
            short_remarks_list.append(short_remarks_dict)
        
        item['short_remarks'] = short_remarks_list
        with open('feiyunzhixia.html', 'wb') as f:
            f.write(response.body)

        yield item