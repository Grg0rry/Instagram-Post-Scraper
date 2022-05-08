from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(5)

email = 'replace with email'
pw = 'replace with password'

login_username = driver.find_element_by_css_selector("input[name='username']")
login_password = driver.find_element_by_css_selector("input[name='password']")
login_username.clear()
login_password.clear()
login_username.send_keys(email)
login_password.send_keys(pw)
driver.find_element_by_css_selector("button[type='submit']").click()

#Skip Pop Up Message
time.sleep(5)
driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
time.sleep(5)
driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()

#Navigate to Tag
tag = "topupshopeepay"
driver.get("https://www.instagram.com/explore/tags/" + tag)

#Scrape
keep_posts = []
while(len(keep_posts) < 120):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(5)
    links = driver.find_elements_by_tag_name('a') #Find post_url and append to list
    for link in links:
        post = link.get_attribute('href')
        if '/p/' in post:
            keep_posts.append(post)
    
#Skip Top Post and Only Select Most Recent
dataset = 100
posts = keep_posts[9:dataset+9]

#Extact Details from post_url (post_url, username, total_likes, and post_upload_date)
df = pd.DataFrame(columns = ['post_url', 'username', 'total_likes', 'post_upload_date'])

for URL in posts:
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source)
    
    #Username
    username = soup.find("a", class_='sqdOP yWX7d _8A5w5 ZIAjV').text
    
    #Like Count
    #No Likes
    if soup.find("div",class_='_7UhW9 xLCgt MMzan KV-D4 uL8Hv T0kll').text == "Be the first to like this":
        total_likes = 0  
    #Hide Like Count
    elif soup.find("div",class_="_7UhW9 xLCgt qyrsm KV-D4 fDxYl T0kll").text == "others" or soup.find("div",class_="_7UhW9 xLCgt qyrsm KV-D4 fDxYl T0kll") is None:
        total_likes = " "
    #Like Count Merged with Text
    elif "like" in soup.find("div",class_="_7UhW9 xLCgt qyrsm KV-D4 fDxYl T0kll").text:
        total_likes = int(str(soup.find("div",class_="_7UhW9 xLCgt qyrsm KV-D4 fDxYl T0kll").text).split(" ")[0])        
    #Normal Extraction of Like Count
    else:
        total_likes = soup.find("div",class_="_7UhW9 xLCgt qyrsm KV-D4 fDxYl T0kll").find_next('span').text
    
    #upload Date
    post_upload_date = soup.find("div",class_="_7UhW9 BARfH MMzan _0PwGv uL8Hv").time.attrs['datetime']
    
    #To DataFrame, to CSV
    df = df.append({'post_url':URL,'username':username,'total_likes':total_likes,'post_upload_date':post_upload_date},
                   ignore_index=True)
    df.to_csv('C:/Users/user/desktop/details.csv')
    