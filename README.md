# 3 Scrapers for ([Goodreads lists](https://www.goodreads.com/list/show/22031.Nonfiction_With_a_Side_of_Self_Help?page=1))

This repository contains web scraping scripts that collect book information from Goodreads. The project is implemented in Python using various libraries and frameworks such as Scrapy and Selenium.

## Installation

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/huseyinpolat-ds/WS_2023_project.git
   ```

2. Navigate to the project directory:

   ```shell
   cd WS_2023_project
   ```

3. Install the required dependencies using pip:

   ```shell
   pip install -r requirements.txt
   ```

   This will install the necessary libraries such as Scrapy, Selenium, pandas, and other dependencies.
   
4. Install the appropriate WebDriver for Selenium:
   
   - The project uses Selenium with Firefox browser in headless mode.
   - Download the appropriate WebDriver for your operating system from the following link: [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
   - Extract the downloaded driver and place it in a directory that is included in your system's PATH environment variable.
   

## Usage

The project consists of multiple web scraping scripts, each serving a specific purpose. Follow the instructions below to run each scraper:

1. Pagination Links Scraper:
   - Open the `pagination_links` directory.
   - Modify the `start_urls` variable in the `links_spider.py` file to specify the Goodreads list URL you want to scrape.
   - Run the scraper using the following command:

     ```shell
     scrapy crawl pagination_links -o pagination_links.csv
     ```

   - The pagination links will be scraped and saved in the `pagination_links.csv` file.

2. Book Links Scraper:
   - Open the `book_links` directory.
   - Place the `pagination_links.csv` file obtained from the previous step in the same directory.
   - Run the scraper using the following command:

     ```shell
     scrapy crawl book_links -o book_links.csv
     ```

   - The book links will be scraped and saved in the `book_links.csv` file.

3. Book Details Scraper:
   - Open the `book_details` directory.
   - Place the `book_links.csv` file obtained from the previous step in the same directory.
   - Run the scraper using the following command:

     ```shell
     scrapy crawl book_details -o book_details.csv
     ```

   - The book details will be scraped and saved in the `book_details.csv` file.

Note: Make sure to have the appropriate CSV files in the respective directories for each scraper to work correctly.

