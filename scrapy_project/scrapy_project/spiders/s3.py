# -*- coding: utf-8 -*-
bool_param = True # When set to True, only first 100 pages will be scraped
import scrapy
from scrapy_splash import SplashRequest 

script1 = """
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(args.wait))
            return {html = splash:html(),
                    url = splash:url()}
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
            if bool_param:
                start_urls = [url.strip() for url in f.readlines()][1:101]
            else:
                start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []
  
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse,endpoint='execute',args={'lua_source': script1,'wait': 0.5, "url" : url, "timeout": 3000, "html" : 1})
 
    def parse(self, response):
        if not response.xpath("//h1[@data-testid = 'bookTitle']/text()").get():
            print("response not valid, making another request")
            yield SplashRequest(response.url, callback=self.parse,dont_filter=True,endpoint='execute',args={'lua_source': script1,'wait': 0.5, "url" : response.url, "timeout": 3000, "html" : 1})
        else:
            p = Book()
            title_element = ("//h1[@data-testid = 'bookTitle']/text()")
            author_name_element = ("//span[contains(@class, 'ContributorLink__name')]/text()")
            author_link_element = ("//a[contains(@class, 'ContributorLink')]/@href")
            average_rating_element = ("//div[@class='BookPageMetadataSection__ratingStats']//div[@class='RatingStatistics__rating']/text()")
            kindle_price_element = ("//span[contains(@class, 'Button__labelItem') and contains(text(), 'Kindle')]/text()")
            rating_count_element = ("//div[@class='BookPageMetadataSection__ratingStats']//span[@data-testid='ratingsCount']/text()")
            review_count_element = ("//div[@class='BookPageMetadataSection__ratingStats']//span[@data-testid='reviewsCount']/text()")
            pages_element = ("//p[@data-testid='pagesFormat']/text()")
            
            p['link'] = response.url
            p['title'] = response.xpath(title_element).get()    
            p['author_name'] = response.xpath(author_name_element).get()
            p['author_link'] = response.xpath(author_link_element).get()
            p['average_rating'] = response.xpath(average_rating_element).get()
            p['kindle_price'] = response.xpath(kindle_price_element).get()
            p['rating_count'] = response.xpath(rating_count_element).get()
            p['review_count'] = response.xpath(review_count_element).get()
            p['n_pages'] = response.xpath(pages_element).get()

            yield p
        
