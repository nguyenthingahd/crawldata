from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

#1 define url
hacker_news_url = 'https://news.ycombinator.com/'

#2 instantiate chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

#3 load the web page
driver.get(hacker_news_url)

#4 wait until element matching the given criteria to be found
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'titleline'))
    )
except:
    driver.quit()

#5 Extract the text value for each title and link in the list
titles= []
links = []

#6 Find all the articles on the web page
story_elements = driver.find_elements(By.CLASS_NAME, 'titleline')

#7 Extract title and link for each article
for story_element in story_elements:

    #8 append title to the titles list
    titles.append(story_element.text)

    #9 extract the URL of the article
    link = story_element.find_element(By.TAG_NAME, "a")

    #10 appen link to the links list
    links.append(link.get_attribute("href"))

# driver.quit()

# save in pandas dataFrame
hacker_news = pd.DataFrame(list(zip(titles, links)),columns=['Title', 'Link'])

# export data into a csv file.
hacker_news.to_csv("hacker_news_data.csv",index=False)


