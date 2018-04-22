from urllib.request import urlopen
from bs4 import BeautifulSoup
import time

stories = []

millis = int(round(time.time()*1000))
base_url = 'https://www.theonion.com/'
satire_url = '%s?startTime=%s'%(base_url,millis)
count = 0

while count < 300:
    page = urlopen(satire_url)
    print("Scraping %s"%(satire_url))
    soup = BeautifulSoup(page, 'html.parser')
    post_list = soup.find("div", class_="post-list--pe")
    feed = post_list.find_all("div", class_="post-wrapper")
    if len(feed) == 0:
        print("No articles, breaking loop")
        break
    for i in feed:
        try:
            article = i.article
            title = article.find("h1", class_="headline")
            url = title.a['href']
            stories.append(url)
            count=count+1
        except Exception as e:
            print(str(e))
    load_more = soup.find("div", class_="load-more__button")
    satire_url = '%s%s'%(base_url, load_more.a['href'])

print("Writing stories")
for story in stories:
    story_soup = BeautifulSoup(urlopen(story), 'html.parser')
    content = story_soup.find("div", class_="main__content")
    article = content.article
    title = article.find("h1", class_="headline")
    try:
        title_text = title.text.strip()
        post_content = article.find("div", class_="post-content")

        f = open("satire/%s.txt"%(title_text.replace(r'[?/-!]', ' ')), "w+b")
        f.write(post_content.text.strip().encode("UTF-8"))
    except Exception as e:
        print(str(e))