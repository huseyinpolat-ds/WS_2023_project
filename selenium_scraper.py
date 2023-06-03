############################# Parameter to limit number of pages
bool_param = True 
cnt = 0 # counter

############################# Libraries

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
import getpass
import datetime
import pandas as pd

gecko_path = '/opt/homebrew/bin/geckodriver'  # directory for gecko driver
ser = Service(gecko_path)
options = webdriver.firefox.options.Options() # get firefox options
options.headless = False

driver = webdriver.Firefox(options = options, service=ser) # use firefox as webdriver/browser

url = 'https://www.goodreads.com/list/show/22031.Nonfiction_With_a_Side_of_Self_Help?page=1' # first url to vist

driver.get(url) # get to given url

# Below query finds the section in the page where links to other pages are located
page_elements  = driver.find_elements(By.XPATH, "//div[@class='pagination']//a") 

# Create empty dataframe to store pagination number and links
pagination_df = pd.DataFrame({'page':[], 'link':[]})
# Manually append first pagination link (current page - visited url)
pagination_df = pagination_df.append({
        'page' : 1,
        'link' : url
    }, ignore_index = True)

# Append each pagination link and text to the pagination dataframe
for element in page_elements:
    page = element.text.strip()
    link = element.get_attribute('href')
    pagination_df = pagination_df.append({
        'page' : page,
        'link' : link
    }, ignore_index = True)

# Empty dataframe to store book links
book_links = pd.DataFrame({'link':[]})

# Below loop goes through each pagination page and extracts links to listed books
# A page holds 100 different book links
for page in pagination_df.loc[0:1,'link']: # We want to limit pagination pages to 2 (first 2 pages), 
                                           # so in total we get no more than 200 book links.
    
    driver.get(page) # visit given pagination page
    time.sleep(3)    # wait for page to load

    try: # Sometimes a flyer pops up and blocks the whole webpage
         # Below query search for this popup and finds close button and clicks on it
         # This is for flyer type 1
        flyer_button = driver.find_element(By.XPATH, '//button[@type="button" and @class = "gr-iconButton"]')
        flyer_button.click()
        time.sleep(1)
    except:
        pass

    try: # Sometimes a flyer pops up and blocks the whole webpage
         # Below query search for this popup and finds close button and clicks on it
         # This is for flyer type 2
        flyer_element = driver.find_element(By.XPATH, "//button[@aria-label = 'Close')]")
        flyer_element.click()
        time.sleep(1)
    except:
        pass

    # Below query finds all links with 'bookTitle'class
    link_element  = driver.find_elements(By.XPATH, "//a[@class='bookTitle']")
    for element in link_element:
        book_link = element.get_attribute("href") # get link from link element
        row = {'link':book_link} 
        book_links = book_links.append(row, ignore_index = True) # append extracted link to book links dataframe

book_links.to_csv('book_links.csv', index=False) # save book links dataframe


# An empty dataframe to store book information
# This dataframe will be filled one-by-one for each book page our crawler visits
books = pd.DataFrame({"link": [], "title": [], "Author Name" : [], "Author Link" : [], "Kindle price" : [],
    "Average rating" : [], "Rating stats:" : [], "N of pages:" : [],
    "Publication info" :[]})

# Iterate through all book links extracted in the previous step
for link in book_links['link']:
    if (bool_param) and (cnt <= 50): # Stop after visiting 100 pages if bool parameter is set to true
            
        driver.get(link) # visit given book link
        cnt += 1  # record number of pages visited
        time.sleep(1) # wait for page to load
            
        try: # Sometimes a flyer pops up and blocks the whole webpage
             # Below query search for this popup and finds close button and clicks on it
             # This is for flyer type 1
            flyer_button = driver.find_element(By.XPATH, '//button[@type="button" and @class = "gr-iconButton"]')
            flyer_button.click()
        except:
            pass

        try: # Sometimes a flyer pops up and blocks the whole webpage
             # Below query search for this popup and finds close button and clicks on it
             # This is for flyer type 2
            flyer_element = driver.find_element(By.XPATH, "//button[@aria-label = 'Close')]")
            flyer_element.click()
        except:
            pass
        
        try: # Below query finds h1 titles with 'bookTitle'class 
             # This is where book title is located
            title_element = driver.find_element(By.XPATH, "//h1[@data-testid = 'bookTitle']")
            title = title_element.text.strip() # get text of given element
        except:
            title = 'Not found'

        try: # Below query finds spans with 'ContributorLink__name'class 
             # This is where the author name is located
            author_name_element = driver.find_element(By.XPATH, "//span[contains(@class, 'ContributorLink__name')]")
            author_name = author_name_element.text.strip() # get text of given element
        except:
            author_name = 'Not found'

        try: # Below query finds the link(s) with 'ContributorLink'class
             # This is where the author link is located
            author_link_element = driver.find_element(By.XPATH, "//a[contains(@class, 'ContributorLink')]")
            author_link = author_link_element.get_attribute('href') # get link from given element
        except:
            author_link = 'Not found'

        try: # Below query finds the span with 'Button__labelItem' class and 'Kindle' in text
             # This is where the kindle price is located
            kindle_price_element = driver.find_elements(By.XPATH, "//span[contains(@class, 'Button__labelItem') and contains(text(), 'Kindle')]")
            kindle_price = kindle_price_element[0].text.strip() # get text of given element
        except:
            kindle_price = 'Not found'

        try: # Below query finds the div with 'RatingStatistics__column' class
             # This is where the average rating is located
            average_rating_element = driver.find_element(By.XPATH, "//div[@class='RatingStatistics__column']")
            average_rating = average_rating_element.text.strip() # get text of given element
        except:
            average_rating = 'Not found'

        try: # Below query finds the div with 'RatingStatistics__meta' class
             # This is where the number of reviews and ratings are located
            rating_stats_element = driver.find_element(By.XPATH, "//div[@class='RatingStatistics__meta']")
            rating_stats = rating_stats_element.text.strip() # get text of given element
        except: 
            rating_stats = 'Not found'

        try: # Below query finds the p with 'pagesFormat' data-testid
             # This is where the number of pages for the book is located
            pages_element = driver.find_element(By.XPATH, "//p[@data-testid='pagesFormat']")
            n_pages = pages_element.text.strip() # get text of given element
        except:
            n_pages = 'Not found'

        try: # Below query finds the p with 'publicationInfo' data-testid
             # This is where the publication details are located
            publication_element = driver.find_element(By.XPATH, "//p[@data-testid='publicationInfo']")
            publication_info = publication_element.text.strip() # get text of given element
        except:
            publication_info = 'Not found'


        # Consolidate all collected data in a dataframe format
        details = pd.DataFrame({"link":[link], "title": title, "Author Name" : [author_name], "Author Link" : [author_link], "Kindle price" : kindle_price,
        "Average rating" : [average_rating], "Rating stats:" : [rating_stats], "N of pages:" : [n_pages],
        "Publication info" :[publication_info]})


        # Append collected details to books dataframe
        books = books.append(details, ignore_index = False)
    else:
        pass

books.to_csv('books.csv', index=False) 