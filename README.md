# Instagram Post Scraper

This scraper is a coded using python to scrape 100 instagram post with the hashtag _#topupshopeepay_ as part of a challenge by Shopee. It uses the library Selenium and BeautifulSoup to mannually go through each instagram post and extract the details like Username, Post_URL, Total_Likes, and Post_Upload_Date.

# Instructions
1. Before running the codes, please ensure that you have the required packages installed. 
	- `pip install selenium`
	- `pip install webdriver-manager`
	- `pip install beautifulsoup4`
	- `pip install pandas`
2. After installation of packages, modify the `email` and `pw` variable with a **valid email address and password** that will able to access and log into Instagram.
3. Lastly change the **file path** in `df.to_csv('C:/Users/user/desktop/details.csv')` to the directory that you  would like the csv file to be stored in.
