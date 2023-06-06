import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import os 
import re 

os.chdir('C:\\Users\\Ankara\\Desktop\\1stclass-2ndsemester\\WS_copy_project\\project\\scrapy_project')

df = pd.read_csv('book_details.csv') # read book links csv

df['rating_count'] = df['rating_count'].str.replace(',', '').astype(int)
df['review_count'] = df['review_count'].str.replace(',', '').astype(int)
df['kindle_price'].fillna(0, inplace = True)
df['kindle_price'] = [float(re.sub(r'[^\d.]+', '', str(price))) for price in df['kindle_price']]
df['average_rating'] = [float(re.sub(r'[^\d.]+', '', str(price))) for price in df['average_rating']]

rating_count = df['rating_count']
review_count = df['review_count']
average_rating = df['average_rating']

print(df.describe().T)



## Avearge rating distribution graph

# df = df[df['average_rating'] > 0]
# plt.hist(df['average_rating'], bins=10)
# plt.xlabel('Average Rating')
# plt.ylabel('Frequency')
# plt.title('Distribution of Average Rating')
# plt.savefig('avg_rating_dist.png', dpi=300)
# plt.show()



## Kindle price distribution graph

# df = df[df['kindle_price'] > 0]
# plt.hist(df['kindle_price'], bins=10)
# plt.xlabel('Kindle Price $')
# plt.ylabel('Frequency')
# plt.title('Distribution of Kindle Price')
# plt.savefig('price_dist.png', dpi=300)
# plt.show()



## Review count graph

# plt.scatter(review_count, average_rating)
# plt.ylabel('Average Rating')
# plt.xlabel('Review Count')
# plt.title('Review Count vs. Average Rating')
# # Create a FuncFormatter to display values in thousands (K) with suffix
# formatter = ticker.FuncFormatter(lambda x, pos: '{:.0f}K'.format(x * 1e-3))
# plt.gca().xaxis.set_major_formatter(formatter)
# plt.xlim(-2000, 60000)
# plt.savefig('review_vs_avg.png', dpi=300)
# plt.show()

## Rating count graph

# plt.scatter(rating_count, average_rating)
# plt.ylabel('Average Rating')
# plt.xlabel('Rating Count')
# plt.title('Rating Count vs. Average Rating')
# # Create a FuncFormatter to display values in thousands (K) with suffix
# formatter = ticker.FuncFormatter(lambda x, pos: '{:.0f}K'.format(x * 1e-3))
# plt.gca().xaxis.set_major_formatter(formatter)
# plt.xlim(-20000, 1000000)
# plt.savefig('rating_vs_avg.png', dpi=300)
# plt.show()




