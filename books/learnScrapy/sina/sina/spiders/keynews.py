# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from sina.items import SinaItem

class KeynewsSpider(scrapy.Spider):
    name = 'keynews'
    allowed_domains = ['crawl']
    start_urls = ['http://news.sina.com.cn/']

    def parse(self, response):
        loader = ItemLoader(item=SinaItem(), response=response)
        loader.add_xpath('centerNews', '//*/h1[@data-client="headline"]/a/text()')
        loader.add_xpath('rightNews', '//*/div[@class="tl"]/a/text()')
        return loader.load_item()
