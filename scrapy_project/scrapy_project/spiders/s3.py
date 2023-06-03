# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest 


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
    name        = scrapy.Field()
    years_active = scrapy.Field()

class LinksSpider(scrapy.Spider):
    name = 'book_details'
    
    custom_settings = {'DOWNLOAD_DELAY': 5}# 2 seconds of delay
    
    
    allowed_domains = ['https://www.goodreads.com/']
    try:
        with open("book_links.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []
        
    def start_requests(self): 
        for url in self.start_urls: 
            yield SplashRequest(url, self.parse, 
                endpoint='render.html', 
                args={'wait': 0.5}, 
           ) 

    def parse(self, response):
        p = Book()
        title_element = ("//h1[@data-testid = 'bookTitle']/text()")
        author_name_element = ("//span[contains(@class, 'ContributorLink__name')]/text()")
        author_link_element = ("//a[contains(@class, 'ContributorLink')]/@href")
        kindle_price_element = ("//span[contains(@class, 'Button__labelItem') and contains(text(), 'Kindle')]/text()")
        average_rating_element = ("//div[@class='BookPageMetadataSection__ratingStats']//div[@class='RatingStatistics__rating']/text()")
        rating_count_element = ("//div[@class='BookPageMetadataSection__ratingStats']//span[@data-testid='ratingsCount']/text()")
        review_count_element = ("//div[@class='BookPageMetadataSection__ratingStats']//span[@data-testid='reviewsCount']/text()")
        pages_element = ("//p[@data-testid='pagesFormat']/text()")
        publication_element = ("//p[@data-testid='publicationInfo']/text()")

        
        p['link'] = response.request.url
        
        try:
            p['title'] = response.xpath(title_element).get()
        except:
            p['title'] = 'Not found'

        p['author_name'] = response.xpath(author_name_element).get()
        p['author_link'] = response.xpath(author_link_element).get()
        p['kindle_price'] = response.xpath(kindle_price_element).get()
        p['average_rating'] = response.xpath(average_rating_element).get()
        p['rating_count'] = response.xpath(rating_count_element).get()
        p['review_count'] = response.xpath(review_count_element).get()
        p['n_pages'] = response.xpath(pages_element).get()
        p['publication_info'] = response.xpath(publication_element).get()

        yield p