import requests
from bs4 import BeautifulSoup
import json
from urllib import parse as urlparse
import unicodedata
import re
import os

_headers = ({'User-Agent':
                 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 '
                 'Safari/537.36',
             'Accept-Language': 'en-US, en;q=0.5'})

_google_search = 'https://google.com/search?'


def get_country():
    return json.loads(requests.get("http://ipinfo.io/json").content.decode("utf-8"))["country"]


def get_services(movie, add=" streaming"):
    req = requests.get(_google_search + urlparse.urlencode({'q': movie + add}), headers=_headers)
    soup = BeautifulSoup(unicodedata.normalize("NFKD", req.content.decode('utf-8')), 'html.parser')

    service_and = {}
    for service in soup.find_all('a', class_='JkUS4b'):
        name = service.find_all('div', class_='i3LlFf')[0].text
        try:
            price = service.find_all('span')[0].text
        except IndexError:
            price = None
        url = service.attrs['href']
        service_and[name] = (price, url)
    return service_and


def is_prime(url, fix_query=True):
    if fix_query:
        parsed = list(urlparse.urlparse(url))
        parsed[4] = ''
        url = urlparse.urlunparse(parsed)

    prime_site = requests.get(url, headers=_headers)
    prime_soup = BeautifulSoup(unicodedata.normalize("NFKD", prime_site.content.decode("utf-8"))
                               .replace("<![endif]-->", ""), 'html.parser')

    logo = prime_soup.find_all('img', class_='_1GFTRr')
    if len(logo) > 0 and "primeLogo" in logo[0].attrs["src"]:
        return True
    else:
        return False


if __name__ == '__main__':
    with open("movies.txt", "r", encoding="utf-8") as file:
        _movie_txt = file.read().splitlines(keepends=False)

    if os.path.exists("movies.json"):
        with open("movies.json", "r", encoding="utf-8") as file:
            _movie_list = json.load(file)
    else:
        _movie_list = {}

    _country = get_country()

    for _movie in _movie_txt:
        _search_obj = re.search(r'\\/--(?P<text>.+)--\\/', _movie)
        if _search_obj is not None:
            _movie_list[_search_obj.group(1)] = None  # shitty implementation...not good practice
        elif _movie != '':
            print(_movie)
            _movie_services = get_services(_movie)
            _subscription = list(filter(lambda f: _movie_services[f][0] is None, _movie_services.keys()))

            if 'Amazon Prime Video' in _movie_services and 'Amazon Prime Video' not in _subscription:
                if is_prime(_movie_services['Amazon Prime Video'][1]):
                    _subscription.append('Amazon Prime Video')

            if _movie not in _movie_list:
                _movie_list[_movie] = {}
            _movie_list[_movie][_country] = _subscription

    with open("movies.json", "w", encoding="utf-8") as file:
        json.dump(_movie_list, file, indent="\t", ensure_ascii=False)
