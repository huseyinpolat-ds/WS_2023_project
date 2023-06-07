# This script scrapes the book links from the specified Goodreads list pages, 
# retrieving the URLs of the books listed on each page.

# Collect book links

# -*- coding: utf-8 -*-
import scrapy

class BookLink(scrapy.Item): # Define fields to be scraped and stored
    book_link = scrapy.Field()

class LinksSpider(scrapy.Spider):
    name = 'book_links' # Spider name

    allowed_domains = ['www.goodreads.com'] # Limiting allowed domain
    try:
        with open("pagination_links.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:] # Retrieve links for all pages
    except:
        start_urls = []

    def parse(self, response):

        xpath = "//a[@class='bookTitle']" # Defining Xpath for element to be scraped
        selection = response.xpath(xpath)
        for s in selection:
            l = BookLink() # Define p as an instance of BookLink class that is defined at the top of this script
            l['book_link'] ='https://www.goodreads.com' + s.xpath('@href').get() # Retrieve href attribute from scraped element and concatanete with domain url
            yield l # Yield l as scraped element