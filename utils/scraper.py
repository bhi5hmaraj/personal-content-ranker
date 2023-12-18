from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import urlopen, Request, ProxyHandler, build_opener
import json
from itertools import cycle
import os
import requests

# Loading the list of proxies for usage with web scraping
proxies = json.loads(open(os.path.abspath('data/proxies.json')).read())
http_proxies = [*proxies['http']]
http_proxies_pool = cycle(http_proxies)

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def scrape_text(url):
    text = ""
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    proxy = next(http_proxies_pool)

    try:
        response = requests.get(
            url,
            headers={
                'User-Agent': user_agent
            },
            # proxies={
            #     'http': f"http://{proxy}"
            # }
        )
        text = text_from_html(response.content)

    except Exception as e:
        print(e)
        print('Failed to fetch', url, 'using proxy', proxy)

    return text