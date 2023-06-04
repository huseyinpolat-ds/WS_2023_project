# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest 
from lxml import etree
import json

script1 = """
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(args.wait))
            while not splash:select('div.RatingStatistics__column') do
                print('waiting')
				assert(splash:go(args.url))
				splash:wait(2)
			end
            return {html = splash:html()}
        end
            """


class Book(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    author_name = scrapy.Field()
    author_link = scrapy.Field()
    kindle_price = scrapy.Field()
    average_rating = scrapy.Field()
    rating_count = scrapy.Field()
    review_count = scrapy.Field()
    n_pages = scrapy.Field()
    publication_info = scrapy.Field()

class LinksSpider(scrapy.Spider):
    name = 'book_details'
    
    
    custom_settings = {
    "SPLASH_URL" : "http://192.168.99.101:8050",

    "DOWNLOADER_MIDDLEWARES" : {
        'scrapy_splash.SplashCookiesMiddleware': 723,
        'scrapy_splash.SplashMiddleware': 725,
        'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    },

    "SPIDER_MIDDLEWARES" : {
        'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
    },

    "DUPEFILTER_CLASS" : 'scrapy_splash.SplashAwareDupeFilter',

    "HTTPCACHE_STORAGE" : 'scrapy_splash.SplashAwareFSCacheStorage'}
    
    
    
    allowed_domains = ['www.goodreads.com']
    try:
        with open("book_links.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []
    

           
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse,endpoint='execute',args={'lua_source': script1,'wait': 5, "url" : url, "timeout": 3000})
            
            
           
    def parse(self, response):
        # parser = etree.HTMLParser()
        # tree = etree.fromstring(response.body, parser)
        p = Book()
        title_element = ("//h1[@data-testid = 'bookTitle']/text()")
        author_name_element = ("//span[contains(@class, 'ContributorLink__name')]/text()")
        author_link_element = ("//a[contains(@class, 'ContributorLink')]/@href")
        average_rating_element = ("//div[@class='BookPageMetadataSection__ratingStats']//div[@class='RatingStatistics__rating']/text()")
        rating_count_element = ("//div[@class='BookPageMetadataSection__ratingStats']//span[@data-testid='ratingsCount']/text()")
        review_count_element = ("//div[@class='BookPageMetadataSection__ratingStats']//span[@data-testid='reviewsCount']/text()")
        pages_element = ("//p[@data-testid='pagesFormat']/text()")
        

        if response.xpath(title_element).get():
            p['link'] = response.request.url
            p['title'] = response.xpath(title_element).get()    
            p['author_name'] = response.xpath(author_name_element).get()
            p['author_link'] = response.xpath(author_link_element).get()
            p['average_rating'] = response.xpath(average_rating_element).get()
            p['rating_count'] = response.xpath(rating_count_element).get()
            p['review_count'] = response.xpath(review_count_element).get()
            p['n_pages'] = response.xpath(pages_element).get()
        else:
            text = response.xpath('//body/script/text()').getall()
            script_piece = response.xpath('//script[contains(text(),"author")]/text()').get()
            p['link'] = 'json'
            p['title'] = text
            p['author_name'] = script_piece

        yield p