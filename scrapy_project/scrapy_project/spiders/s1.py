# This script scrapes the pagination links from the specified 
# Goodreads list and extracts the page number and corresponding URL for each page.

# Collect pagination links

# -*- coding: utf-8 -*-
import scrapy

class PaginationLink(scrapy.Item): # Define fields to be scraped and stored
    page = scrapy.Field()
    link = scrapy.Field()

class LinkListsSpider(scrapy.Spider):
    name = 'pagination_links' # Spider name
    allowed_domains = ['www.goodreads.com'] # Limiting allowed domain
    start_urls = ['https://www.goodreads.com/list/show/22031.Nonfiction_With_a_Side_of_Self_Help?page=1'] # Starting page url

    def parse(self, response):
        xpath = "//div[@class='pagination']//a" # Defining Xpath for element to be scraped
        selection = response.xpath(xpath)

        p0 = PaginationLink() # Define p0 as an instance of PaginationLink class that is defined at the top of

        p0['page'] = '1' # Manually entering page number
        p0['link'] = response.url # Retrive scraped link = start_urls

        yield p0 # Yield p0 as scraped element -- this yield is done manually in order to have 1st page in the output csv

        for s in selection:
            p = PaginationLink() # Define p as an instance of PaginationLink class that is defined at the top of
            
            page_n = s.xpath('text()').get() # Retrieve the text from scraped element
        
            if len(page_n) <= 2: # This condition simply checks if given page number text has maximum of 2 characters
                                 # There is a duplicate link for page 2 under '2' and '-> next'
                                 # This condition will filter the duplicate entry with '-> next'
              p['page'] = page_n
              p['link'] = 'https://www.goodreads.com' + s.xpath('@href').get() # Retrieve href attribute from scraped element and concatanete with domain url
            else:
              pass
            
            yield p # Yield p as scraped element