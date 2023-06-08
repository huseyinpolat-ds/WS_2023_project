import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import re

# Parameter to limit number of pages
bool_param = True
cnt = 0  # counter

# Collect pagination links

url = 'https://www.goodreads.com/list/show/22031.Nonfiction_With_a_Side_of_Self_Help?page=1'  # first url to visit

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

## Create empty dataframe to store pagination number and links
pagination_df = pd.DataFrame(columns=['page', 'link'])
## Manually append first pagination link (current page - visited url)
pagination_df = pd.concat([pagination_df, pd.DataFrame({'page': [1], 'link': [url]})], ignore_index=True)

## Find all pagination links and extract page number and corresponding URL
pagination_links = soup.select('div.pagination a')
for link in pagination_links:
    page = link.text.strip()
    link_url = 'https://www.goodreads.com' + link['href']
    if len(page) <= 2:
        pagination_df = pd.concat([pagination_df, pd.DataFrame({'page': [page], 'link': [link_url]})], ignore_index=True)
    else:
        pass


pagination_df.to_csv('C:\\Users\\Gizem\\Desktop\\UW\\2nd\\WEB_SCRAPING\\PROJECT\\BS\\pagination_links.csv', index=False)  # save pagination links dataframe

# Collect book links

pagination_df = pd.read_csv('pagination_links.csv')  # read pagination links csv

## Empty dataframe to store book links
book_links = pd.DataFrame(columns=['link'])

## Iterate through each pagination page and extract links to listed books
for _, row in pagination_df.iterrows():
    page = row['link']
    response = requests.get(page)
    soup = BeautifulSoup(response.content, 'html.parser')

    print("Pagination", row['page'], page)

    ### Find all book links on the page
    links = soup.select('a.bookTitle')
    for link in links:
        book_link = 'https://www.goodreads.com' + link['href']
        row = pd.DataFrame({'link': [book_link]})
        book_links = pd.concat([book_links, row], ignore_index=True)

book_links.to_csv('C:\\Users\\Gizem\\Desktop\\UW\\2nd\\WEB_SCRAPING\\PROJECT\\BS\\book_links.csv', index=False)  # save book links dataframe

## Collect book details

book_links = pd.read_csv('book_links.csv')  # read book links csv

if bool_param:  # Read only links for the first 100 pages if the bool parameter is set to True
    book_links = book_links[1:101]

# An empty dataframe to store book information
# This dataframe will be filled one-by-one for each book page our crawler visits
books = pd.DataFrame(columns=["link", "title", "author_name", "author_link", "kindle_price",
                              "average_rating", "rating_count", "review_count", "n_pages"])

# Function to parse book details from a given URL
def parse_book_details(url):
    response = None
    while response is None:
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException:
            print(f"Request failed for {url}. Retrying...")
            time.sleep(1)

    soup = BeautifulSoup(response.content, 'html.parser')
    time.sleep(1)
    
    try:
        # Get book title
        title_element = soup.find('h1', attrs={'data-testid': 'bookTitle'})
        title = title_element.text.strip() if title_element else ''
    except:
        title = ''
    
    try:
        # Get author name
        author_name_element = soup.find('span', class_='ContributorLink__name')
        author_name = author_name_element.text.strip() if author_name_element else ''
    except:
        author_name = ''
    
    try:
        # Get author link
        author_link_element = soup.find('a', class_='ContributorLink')
        author_link = author_link_element['href'] if author_link_element else ''
    except:
        author_link = ''
    
    try:
        # Get Kindle price
        kindle_price_element = soup.find('span', class_='Button__labelItem', text='Kindle')
        kindle_price = kindle_price_element.text.strip() if kindle_price_element else ''
    except:
        kindle_price = ''
    
    try:
        # Get average rating
        average_rating_element = soup.find('div', class_='RatingStatistics__column')
        average_rating = average_rating_element.text.strip() if average_rating_element else ''
    except:
        average_rating = ''
    
    try:
        # Get rating count
        rating_count_element = soup.find('div', class_='BookPageMetadataSection__ratingStats').find('span', {'data-testid': 'ratingsCount'})
        rating_count = rating_count_element.text.strip() if rating_count_element else ''
    except:
        rating_count = ''
    
    try:
        # Get review count
        review_count_element = soup.find('div', class_='BookPageMetadataSection__ratingStats').find('span', {'data-testid': 'reviewsCount'})
        review_count = review_count_element.text.strip() if review_count_element else ''
    except:
        review_count = ''
    
    try:
        # Get number of pages
        pages_element = soup.find('p', attrs={'data-testid': 'pagesFormat'})
        n_pages = pages_element.text.strip() if pages_element else ''
    except:
        n_pages = ''
    
    # Consolidate all collected data in a dataframe format
    details = pd.DataFrame({"link": [url], "title": [title], "author_name": [author_name],
                            "author_link": [author_link], "kindle_price": [kindle_price],
                            "average_rating": [average_rating], "rating_count": [rating_count],
                            "review_count": [review_count], "n_pages": [n_pages]})

    return details

# Iterate through all book links extracted in the previous step
for link in book_links['link']:
    details = parse_book_details(link)
    
    # Retry until the desired element (title) is found or until the website response is valid
    while details['title'].values[0] == '':
        print(f"Title not found for {link}. Retrying...")
        details = parse_book_details(link)

    # Append collected details to books dataframe
    books = pd.concat([books, details], ignore_index=False)

    print("Book", link)

# Final data manipulation

# Apply the regex pattern to the 'rating_count' and 'review_count' column
pattern = r'[^0-9,]'  # Regex pattern to match
books['rating_count'] = books['rating_count'].apply(lambda x: re.sub(pattern, '', x))
books['review_count'] = books['review_count'].apply(lambda x: re.sub(pattern, '', x))

books.to_csv('C:\\Users\\Gizem\\Desktop\\UW\\2nd\\WEB_SCRAPING\\PROJECT\\BS\\book_details.csv', index=False)  # save scraped book details to CSV file
