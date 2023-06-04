# Collect pagination links
# -*- coding: utf-8 -*-
import scrapy

class PaginationLink(scrapy.Item):
    link = scrapy.Field()

class LinkListsSpider(scrapy.Spider):
    name = 'pagination_links'
    allowed_domains = ['www.goodreads.com']
    start_urls = ['https://www.goodreads.com/list/show/22031.Nonfiction_With_a_Side_of_Self_Help?page=1']

    def parse(self, response):
        xpath = "//div[@class='pagination']//a"
        selection = response.xpath(xpath)
        for s in selection:
            p = PaginationLink()
            page_n = s.xpath('text()').get()
            
            if len(page_n) <= 2:
              p['link'] = 'https://www.goodreads.com' + s.xpath('@href').get()
            else:
              pass
            
            yield p