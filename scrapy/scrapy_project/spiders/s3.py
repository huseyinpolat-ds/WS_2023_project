# This script performs web scraping to extract book details 
# from the provided URLs, and it handles cases where the desired 
# element is not available in the response by making another request.

# Collect book details

# -*- coding: utf-8 -*-
bool_param = True # When set to True, only first 100 pages will be scraped
import scrapy
from scrapy import Request

class Book(scrapy.Item): # Define fields to be scraped and stored
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
    name = 'book_details' # Spider name
    
    allowed_domains = ['www.goodreads.com'] # Limiting allowed domain
    
    try:
        with open("book_links.csv", "rt") as f:
            if bool_param:
                start_urls = [url.strip() for url in f.readlines()][1:101] # Retrieve links for first 100 pages if bool parameter is true
            else:
                start_urls = [url.strip() for url in f.readlines()][1:] # Otherwise, retrieve links for all pages 
    except:
        start_urls = []
  
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse) # Raise a request to website for each link we read in previous step
                                                    # Call self.parse() method after
 
    def parse(self, response):
        if not response.xpath("//h1[@data-testid = 'bookTitle']/text()").get(): # Checking if desired xpath element is available in the response
            print("response not valid, making another request")
            yield Request(response.url, callback=self.parse, dont_filter=True) # If not, making another request for the same link
                                                                               # dont_filter parameter is set to True for our request
                                                                               # to not to be filtered by the scheduler - identical url calls are
                                                                               # automatically filtered by scrapy
            
        else:
            p = Book() # Define p as an instance of Book class that is defined at the top of this script
            
            # Defining Xpaths for each element to be scraped
            title_element = ("//h1[@data-testid = 'bookTitle']/text()")            
            author_name_element = ("//span[contains(@class, 'ContributorLink__name')]/text()")
            author_link_element = ("//a[contains(@class, 'ContributorLink')]/@href")
            average_rating_element = ("//div[@class='BookPageMetadataSection__ratingStats']//div[@class='RatingStatistics__rating']/text()")
            kindle_price_element = ("//span[contains(@class, 'Button__labelItem') and contains(text(), 'Kindle')]/text()")
            rating_count_element = ("//div[@class='BookPageMetadataSection__ratingStats']//span[@data-testid='ratingsCount']/text()")
            review_count_element = ("//div[@class='BookPageMetadataSection__ratingStats']//span[@data-testid='reviewsCount']/text()")
            pages_element = ("//p[@data-testid='pagesFormat']/text()")
            
            p['link'] = response.url # Get scraped url to save

            # Other scraped elements
            p['title'] = response.xpath(title_element).get()    
            p['author_name'] = response.xpath(author_name_element).get()
            p['author_link'] = response.xpath(author_link_element).get()
            p['average_rating'] = response.xpath(average_rating_element).get()
            p['kindle_price'] = response.xpath(kindle_price_element).get()
            p['rating_count'] = response.xpath(rating_count_element).get()
            p['review_count'] = response.xpath(review_count_element).get()
            p['n_pages'] = response.xpath(pages_element).get()

            yield p # Yield p as scraped element
			
    def close(self, reason):
        start_time = self.crawler.stats.get_value('start_time')
        finish_time = self.crawler.stats.get_value('finish_time')
        print("Total run time: ", finish_time-start_time)
