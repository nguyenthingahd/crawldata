import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
import requests
import shutil
import os
import validators
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',}
http = httplib2.Http()

def Get_Text(url): 
    saved_dir = 'Text'

    if not os.path.exists(saved_dir):
        os.mkdir(saved_dir)

    try:
        response = urllib.request.urlopen(url)      # make request with https url
        time.sleep(5)
    except:
        status, response = http.request(url)        # make request with http url
    soup = BeautifulSoup(response, 'html.parser')
    print(soup)
    
    #create a crawled file with website title name
    
    file_content = ""
    content = soup.find_all('p') #['h1','h2','h3','h4','div','p'])      

    if len(content) == 0:
        print("There is nothing to crawl")
        exit()
    file_text =os.path.join(saved_dir, soup.title.string + ".txt")
    with open(file_text, "w", encoding="utf-8") as f:
        print("Website title:"+ soup.title.string)
        print("Text content:")

        for feed in content:
            file_content += feed.get_text() + " "
        print(file_content)
        f.write(file_content)
        f.close()
    
    print("Crawling text succeeded!")

def Get_Img(url):
    saved_dir = 'Img'

    if not os.path.exists(saved_dir):
        os.mkdir(saved_dir)

    count_img = 0
    count_download = 0
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    
    # Specify the path to the ChromeDriver executable
    chromedriver_path = '/usr/bin/chromedriver'
    
    # Create a Service object
    service = Service(chromedriver_path)
    
    # Initialize the WebDriver with the Service object
    browser = webdriver.Chrome(service=service, options=options)
    browser.get(url)
    images = browser.find_elements(By.TAG_NAME, 'img')
    for image in images:
        image_url = image.get_attribute('src')
        print(image_url)
        try:
            if not validators.url(image_url):
                image_url = url + image_url.split('//')[0]
            r = requests.get(image_url, stream=True, headers=headers)
            print("Status code: " + str(r.status_code))
            if r.status_code == 200:
                filename = os.path.join(saved_dir, image_url.split('/')[-1])
                with open(filename, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    count_download += 1
        except Exception as e:
            print("Cannot download: " + str(image_url) + " due to: " + str(e))
    print("Crawling img succeeded!")

url = str(input('URL: '))

# if url[len(url)-1] != '/':  #url standardization
#     url += '/'
# if 'https://' not in url and 'http://' not in url:
#     url = 'https://' + url

Get_Text(url)
time.sleep(5)
# Get_Img(url)
# time.sleep(5)