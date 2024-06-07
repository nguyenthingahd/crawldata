import requests
from bs4 import BeautifulSoup
listlink = []
def crawl(baseUrl, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.findAll('ul', class_='list')
    # print(titles)
    
    links = [link.find('a') for link in titles]
    # import pdb; pdb.set_trace()
    for link in links:
        if link not in listlink:
            listlink.append(link)
            try:
                print(link)
                news = requests.get(baseUrl + link)
                print(news)
                soup = BeautifulSoup(news.content, "html.parser")
                body = soup.find("div", class_="col-md-7 middle-cols")
             
                text = ""
                content = body.findChildren("b", recursive=False)
                text_file = open("datals.txt", "a")
                for i in range(0, len(content)):
                    str = content[i].text
                    sentences = str.split(".")
                    for text in sentences:
                        if len(text) > 1 and len(text) < 190:
                            text = text.replace("- ", "")
                            text = text.replace("\"", "")
                            text = text.strip()
                            text = text + ".\n"
                            text_file.write(text)
                text_file.close()
            except:
                pass
if __name__ == "__main__":
    f = open("url.txt")
    str = f.read()
    lst = str.split("\n")
    print(lst)
    baseUrl = "https://www.vietjack.com/bai-tap-trac-nghiem-dia-li-12/"
    for url in lst:
        crawl(baseUrl, url)
        # for i in range (2, 10):
        #     urll = url[:-4] + '/trang-{}.htm'.format(i)
        #     crawl(baseUrl, urll)