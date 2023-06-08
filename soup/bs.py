import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor

# Parameter to limit the number of pages
bool_param = True

start_time = time.time()

# Create an instance of requests.Session for efficient network requests
session = requests.Session()

# Collect pagination links
url = 'https://www.goodreads.com/list/show/22031.Nonfiction_With_a_Side_of_Self_Help?page=1'
response = session.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

pagination_links = soup.select('div.pagination a')
pagination_df = pd.DataFrame(columns=['page', 'link'])
pagination_df = pd.concat([pagination_df, pd.DataFrame({'page': [1], 'link': [url]})], ignore_index=True)

for link in pagination_links:
    page = link.text.strip()
    link_url = 'https://www.goodreads.com' + link['href']
    if len(page) <= 2:
        pagination_df = pd.concat([pagination_df, pd.DataFrame({'page': [page], 'link': [link_url]})], ignore_index=True)

pagination_df.to_csv('C:\\Users\\Gizem\\Desktop\\UW\\2nd\\WEB_SCRAPING\\PROJECT\\BS\\pagination_links.csv', index=False)

# Collect book links
pagination_df = pd.read_csv('C:\\Users\\Gizem\\Desktop\\UW\\2nd\\WEB_SCRAPING\\PROJECT\\BS\\pagination_links.csv')
book_links = pd.DataFrame(columns=['link'])

def extract_book_links(page):
    response = session.get(page)
    soup = BeautifulSoup(response.content, 'html.parser')
    print("Pagination", page)

    links = soup.select('a.bookTitle')
    book_links = []
    for link in links:
        book_link = 'https://www.goodreads.com' + link['href']
        book_links.append(book_link)
    return book_links

with ThreadPoolExecutor() as executor:
    results = executor.map(extract_book_links, pagination_df['link'])
    for result in results:
        book_links = pd.concat([book_links, pd.DataFrame({'link': result})], ignore_index=True)

book_links.to_csv('C:\\Users\\Gizem\\Desktop\\UW\\2nd\\WEB_SCRAPING\\PROJECT\\BS\\book_links.csv', index=False)

# Collect book details
book_links = pd.read_csv('C:\\Users\\Gizem\\Desktop\\UW\\2nd\\WEB_SCRAPING\\PROJECT\\BS\\book_links.csv')
if bool_param:
    book_links = book_links[1:101]

books = pd.DataFrame(columns=["link", "title", "author_name", "author_link", "kindle_price",
                              "average_rating", "rating_count", "review_count", "n_pages"])

def parse_book_details(url):
    response = None
    while response is None:
        try:
            response = session.get(url)
        except requests.exceptions.RequestException:
            print(f"Request failed for {url}. Retrying...")
            time.sleep(1)

    soup = BeautifulSoup(response.content, 'html.parser')
    time.sleep(1)
    
    try:
        title_element = soup.find('h1', attrs={'data-testid': 'bookTitle'})
        title = title_element.text.strip() if title_element else ''
    except:
        title = ''
    
    try:
        author_name_element = soup.find('span', class_='ContributorLink__name')
        author_name = author_name_element.text.strip() if author_name_element else ''
    except:
        author_name = ''
    
    try:
        author_link_element = soup.find('a', class_='ContributorLink')
        author_link = author_link_element['href'] if author_link_element else ''
    except:
        author_link = ''
    
    try:
        kindle_price_element = soup.find('span', class_='Button__labelItem', text=re.compile(r'Kindle'))
        kindle_price = kindle_price_element.text.strip() if kindle_price_element else ''
    except:
        kindle_price = ''

    
    try:
        average_rating_element = soup.find('div', class_='RatingStatistics__column')
        average_rating = average_rating_element.text.strip() if average_rating_element else ''
    except:
        average_rating = ''
    
    try:
        rating_count_element = soup.find('div', class_='BookPageMetadataSection__ratingStats').find('span', {'data-testid': 'ratingsCount'})
        rating_count = rating_count_element.text.strip() if rating_count_element else ''
    except:
        rating_count = ''
    
    try:
        review_count_element = soup.find('div', class_='BookPageMetadataSection__ratingStats').find('span', {'data-testid': 'reviewsCount'})
        review_count = review_count_element.text.strip() if review_count_element else ''
    except:
        review_count = ''
    
    try:
        pages_element = soup.find('p', attrs={'data-testid': 'pagesFormat'})
        n_pages = pages_element.text.strip() if pages_element else ''
    except:
        n_pages = ''
    
    details = pd.DataFrame({"link": [url], "title": [title], "author_name": [author_name],
                            "author_link": [author_link], "kindle_price": [kindle_price],
                            "average_rating": [average_rating], "rating_count": [rating_count],
                            "review_count": [review_count], "n_pages": [n_pages]})

    return details


def scrape_book_details(link):
    details = parse_book_details(link)

    while details['title'].values[0] == '':
        print(f"Title not found for {link}. Retrying...")
        details = parse_book_details(link)

    return details

with ThreadPoolExecutor() as executor:
    results = executor.map(scrape_book_details, book_links['link'])
    for result in results:
        books = pd.concat([books, result], ignore_index=False)
        print("Book", result['link'].values[0])

# Final data manipulation
pattern = r'[^0-9,]'
books['rating_count'] = books['rating_count'].apply(lambda x: re.sub(pattern, '', x))
books['review_count'] = books['review_count'].apply(lambda x: re.sub(pattern, '', x))

books.to_csv('C:\\Users\\Gizem\\Desktop\\UW\\2nd\\WEB_SCRAPING\\PROJECT\\BS\\book_details.csv', index=False)

end_time = time.time()
total_time = end_time - start_time
print("Scraping time:", total_time, "seconds")
