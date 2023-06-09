############################# Parameter to limit number of pages
bool_param = True
cnt = 0 # counter
############################# Libraries

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import getpass
import pandas as pd
import re

##get start time for calculation scraping time 
start_time = time.time()

gecko_path = '/opt/homebrew/bin/geckodriver'  # directory for gecko driver
ser = Service(gecko_path)
options = webdriver.firefox.options.Options() # get firefox options
options.add_argument("--headless")

driver = webdriver.Firefox(options = options, service=ser) # use firefox as webdriver/browser

############################# Collect pagination links

# This piece of script scrapes the pagination links from the specified 
# Goodreads list and extracts the page number and corresponding URL for each page.

url = 'https://www.goodreads.com/list/show/22031.Nonfiction_With_a_Side_of_Self_Help?page=1' # first url to vist

driver.get(url) # get to given url

# Create empty dataframe to store pagination number and links
pagination_df = pd.DataFrame(columns=['page', 'link'])
# Manually append first pagination link (current page - visited url)
pagination_df = pd.concat([pagination_df, pd.DataFrame({'page': [1], 'link': [url]})], ignore_index=True)

# Below query finds the section in the page where links to other pages are located
page_elements  = driver.find_elements(By.XPATH, "//div[@class='pagination']//a") 

# Append each pagination link and text to the pagination dataframe
for element in page_elements:
    page = element.text.strip()
    link = element.get_attribute('href')
    if len(page) <= 2:
        pagination_df = pd.concat([pagination_df, pd.DataFrame({'page': [page], 'link': [link]})], ignore_index=True)
    else:
        pass

pagination_df.to_csv('pagination_links.csv', index=False) # save pagination links dataframe

############################# Collect book links

# This piece of script scrapes the book links from the specified Goodreads list pages, 
# retrieving the URLs of the books listed on each page.

pagination_df = pd.read_csv('pagination_links.csv') # read pagination links csv

# Empty dataframe to store book links
book_links = pd.DataFrame(columns=['link'])

# Below loop goes through each pagination page and extracts links to listed books
# A page holds 100 different book links
for page in pagination_df['link']:
                                   
    driver.get(page) # visit given pagination page
    time.sleep(0.5) # wait for page to load


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

    # Below query finds all links with 'bookTitle'class
    link_element  = driver.find_elements(By.XPATH, "//a[@class='bookTitle']")
    
    print("Pagination ", pagination_df.loc[pagination_df['link'] == page, 'page'].values[0], page)

    for element in link_element:
        book_link = element.get_attribute("href") # get link from link element
        row = pd.DataFrame({'link':[book_link]} )
        book_links = pd.concat([book_links, row], ignore_index=True) # append extracted link to book links dataframe

book_links.to_csv('book_links.csv', index=False) # save book links dataframe


############################# Collect book details

# This piece of script performs web scraping to extract book details 
# from the provided URLs.

book_links = pd.read_csv('book_links.csv') # read book links csv

if bool_param: # Read only links for first 100 pages if bool parameter is set to true
    book_links = book_links[1:101]

# An empty dataframe to store book information
# This dataframe will be filled one-by-one for each book page our crawler visits
books = pd.DataFrame(columns=["link", "title", "author_name", "author_link", "kindle_price",
    "average_rating", "rating_count", "review_count", "n_pages"])

# Iterate through all book links extracted in the previous step
for link in book_links['link']:
            
    driver.get(link) # visit given book link
    time.sleep(0.5)
    cnt += 1  # record number of pages visited
    
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
        title = ''

    try: # Below query finds spans with 'ContributorLink__name'class 
            # This is where the author name is located
        author_name_element = driver.find_element(By.XPATH, "//span[contains(@class, 'ContributorLink__name')]")
        author_name = author_name_element.text.strip() # get text of given element
    except:
        author_name = ''

    try: # Below query finds the link(s) with 'ContributorLink'class
            # This is where the author link is located
        author_link_element = driver.find_element(By.XPATH, "//a[contains(@class, 'ContributorLink')]")
        author_link = author_link_element.get_attribute('href') # get link from given element
    except:
        author_link = ''

    try: # Below query finds the span with 'Button__labelItem' class and 'Kindle' in text
            # This is where the kindle price is located
        kindle_price_element = driver.find_elements(By.XPATH, "//span[contains(@class, 'Button__labelItem') and contains(text(), 'Kindle')]")
        kindle_price = kindle_price_element[0].text.strip() # get text of given element
    except:
        kindle_price = ''

    try: # Below query finds the div with 'RatingStatistics__column' class
            # This is where the average rating is located
        average_rating_element = driver.find_element(By.XPATH, "//div[@class='RatingStatistics__column']")
        average_rating = average_rating_element.text.strip() # get text of given element
    except:
        average_rating = ''


    try: # Below query finds the div with 'BookPageMetadataSection__ratingStats' class and
            # 'ratingsCount' span, which is a child of the previous div
            # This is where the rating count is located
        rating_count_element = driver.find_element(By.XPATH,"//div[@class='BookPageMetadataSection__ratingStats']//span[@data-testid='ratingsCount']")
        rating_count = rating_count_element.text.strip() # get text of given element
    except:
        rating_count = ''

    try: # Below query finds the div with 'BookPageMetadataSection__ratingStats' class and
            # 'reviewsCount' span, which is a child of the previous div
            # This is where the review count is located
        review_count_element = driver.find_element(By.XPATH,"//div[@class='BookPageMetadataSection__ratingStats']//span[@data-testid='reviewsCount']")
        review_count = review_count_element.text.strip() # get text of given element
    except:
        review_count = ''

    try: # Below query finds the p with 'pagesFormat' data-testid
            # This is where the number of pages for the book is located
        pages_element = driver.find_element(By.XPATH, "//p[@data-testid='pagesFormat']")
        n_pages = pages_element.text.strip() # get text of given element
    except:
        n_pages = ''

    # Consolidate all collected data in a dataframe format
    details = pd.DataFrame({"link":[link], "title": [title], "author_name" : [author_name], 
                            "author_link" : [author_link], "kindle_price" : [kindle_price],
                            "average_rating" : [average_rating], "rating_count" : [rating_count], 
                            "review_count" : [review_count], "n_pages" :[n_pages]})

    # Append collected details to books dataframe
    books = pd.concat([books, details], ignore_index = False)

    print("Book ", cnt, link)


# Final data manipulation

# Apply the regex pattern to the 'rating_count' and 'review_count' column

pattern = r'[^0-9,]' # Regex pattern to match

books['rating_count'] = books['rating_count'].apply(lambda x: re.sub(pattern, '', x)) # Remove ' ratings' text and leave only digits and comma
books['review_count'] = books['review_count'].apply(lambda x: re.sub(pattern, '', x)) # Remove ' reviews' text and leave only digits and comma

books.to_csv('book_details.csv', index=False) # save scraped book details to csv file

#get the end time and calculate scraping time in Seconds
end_time = time.time()
total_time = end_time - start_time
print("Scraping time:", total_time, "seconds")
