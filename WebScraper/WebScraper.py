from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin
import urllib.request
import colorama


colorama.init()
green = colorama.Fore.GREEN
yellow = colorama.Fore.YELLOW
gray = colorama.Fore.LIGHTBLACK_EX
red = colorama.Fore.RED
reset = colorama.Fore.RESET

internal_urls = set()
external_urls = set()

def Check(url):
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        if response.status in [204, 301, 308, 400, 401, 404, 408, 410, 500, 501, 502]:
            print(red + response.status + " - " + response.reason + " --> " + url)
        else:
            print(green + " no problem in --> " + url)
    except Exception as exception:
        print(yellow + " {}-{} ".format(exception, url))
        pass

def is_valid(url):
    parsed= urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_links(url):
    urls = set()
    domain = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue

        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + ("://") + parsed_href.netloc + parsed_href.path

        if not is_valid(href):
            continue
        if href in internal_urls:
            continue
        if domain not in href:
            if href not in external_urls:
                Check(href)
                external_urls.add(href)
            continue
        Check(href)
        urls.add(href)
        internal_urls.add(href)

    return urls


total_urls = 0

def crawl(url, max_urls=30):
    global total_urls
    total_urls += 1
    links = get_links(url)
    for link in links:
        if total_urls > max_urls:
            break
        crawl(link, max_urls=max_urls)


if __name__ == "__main__":

    URL = input("please enter a url:  ")
    crawl(URL)
    print("Total links: ", len(external_urls) + len(internal_urls))
  



