# -*- coding: utf-8 -*-
import scrapy

class BookLink(scrapy.Item):
    book_link = scrapy.Field()

class LinksSpider(scrapy.Spider):
    name = 'book_links'
    allowed_domains = ['www.goodreads.com']
    try:
        with open("pagination_links.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []

    def parse(self, response):
        print(response)
        xpath = "//a[@class='bookTitle']"
        selection = response.xpath(xpath)
        for s in selection:
            l = BookLink()
            l['book_link'] ='https://www.goodreads.com' + s.xpath('@href').get()
            yield l