import requests
from bs4 import BeautifulSoup
listlink = []
def crawl(baseUrl, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.findAll('h3', class_='verticalPost__main-title vnn-title title-bold')
    links = [link.find('a').attrs["href"] for link in titles]
    
    for link in links:
        if link not in listlink:
            listlink.append(link)
            try:
                print(link)
                import pdb; pdb.set_trace()
                news = requests.get(link)
                soup = BeautifulSoup(news.content, "html.parser")
                body = soup.find("div", class_="page")
                text = ""
                content = body.findChildren("p", recursive=False)
                text_file = open("data.txt", "a")
                for i in range(0, len(content)):
                    str = content[i].text
                    sentences = str.split(".")
                    for text in sentences:
                        if len(text) > 1 and len(text) < 190:
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
    baseUrl = "https://vietnamnet.vn/en"
    for url in lst:
        crawl(baseUrl, url)
        for i in range(2, 10):
            urll = f"{baseUrl}/-page{i}"  # Use f-string to format the URL
            crawl(baseUrl, urll)

