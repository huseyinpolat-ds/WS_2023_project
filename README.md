# 3 Scrapers for [Goodreads lists](https://www.goodreads.com/list/show/22031.Nonfiction_With_a_Side_of_Self_Help?page=1)

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
   - Download the appropriate WebDriver for your operating system from the following link: [GeckoDriver for Firefox](https://github.com/mozilla/geckodriver/releases)
   - Extract the downloaded driver and place it in a directory that is included in your system's PATH environment variable.

## Selenium Usage

Before running the script, you may need to modify some configuration variables according to your requirements. These variables are typically located at the beginning of the script file and are marked with comments for easy identification. Here are some common variables you might need to configure:

- `WEB_DRIVER_PATH`: Set this variable to the path of the web driver executable on your machine.
- `BROWSER`: Specify the browser you want to automate (e.g., "chrome" or "firefox").
-  Modify the first `url` variable to specify the Goodreads list URL you want to scrape.

### Running the Script
1. Open a terminal or command prompt.
2. Navigate to the directory where the script is located.
3. Execute the following command to run the script:
   ```
   python selenium_scraper.py
   ```
   Replace `script_name.py` with the actual name of the script file.

Once the script starts running, it will automate the specified browser and perform the desired actions based on the provided instructions.

## Scrapy Usage

The project consists of multiple web scrapy spiders, each serving a specific purpose. Follow the instructions below to run each scraper:

1. Pagination Links Scraper:
   - Open the `spiders` directory.
   - Modify the `start_urls` variable in the `s1.py` file to specify the Goodreads list URL you want to scrape.
   - Run the scraper using the following command:

     ```shell
     scrapy crawl pagination_links -o pagination_links.csv
     ```

   - The pagination links will be scraped and saved in the `pagination_links.csv` file.

2. Book Links Scraper:
   - Run the scraper using the following command:

     ```shell
     scrapy crawl book_links -o book_links.csv
     ```

   - The book links will be scraped and saved in the `book_links.csv` file.

3. Book Details Scraper:
   - Run the scraper using the following command:

     ```shell
     scrapy crawl book_details -o book_details.csv
     ```

   - The book details will be scraped and saved in the `book_details.csv` file.

Note: Make sure to have the exact same CSV file naming as in instructions in 2nd and 3rd spider to work correctly.

