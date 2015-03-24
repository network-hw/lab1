#-*-coding:utf-8-*-
#######################################
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from danhuaer.items import DanhuaerItem
import re
from scrapy.http import Request
from scrapy.selector import Selector

class DanhuaerSpider(CrawlSpider):
	name="danhuaer"
	allowed_domains = ["danhuaer.com"]
	start_urls = ["http://danhuaer.com/?o=top"]
	rules = (Rule(SgmlLinkExtractor(allow=('/t/\d*')),  callback = 'parse_img', follow=True),)
	def parse_img(self, response):
		urlItem = DanhuaerItem()
		sel = Selector(response)
		for divs in sel.xpath('//div[@class="post-container"]'):
		    img_url=divs.xpath('.//img/@data-original').extract()[0]
		    urlItem['url'] = img_url
		    yield urlItem
