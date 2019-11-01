# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter

class DoubanspiderPipeline(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file = open('top250.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()


    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item



class AllMusicPipeline(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file = open('allmuisc.txt', 'w')
    

    def close_spider(self, spider):
        self.file.close()


    def process_item(self, item, spider):
        self.file.write(item['url'] + '\n')
        return item