# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from danhuaer.items import DanhuaerItem

class DanhuaerPipeline(object):
    def __init__(self):
        self.mfile = open('test.html', 'w')
    def process_item(self, item, spider):
        text = '<img src="' + item['url'] + '" alt = "" />'
        self.mfile.writelines(text)
    def close_spider(self, spider):
        self.mfile.close()
       # return item
