import re
from urllib import parse

import requests

class ImageDownloader():
    BASE_URL = 'https://google.com'
    ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'webp', 'png']

    def __init__(self) -> None:
        self.pages = []
        self.current_page = 0

    def query(self, query = None, page = 0):
        if query is None:
            return []

        if len(self.pages) > (page + 1):
            return self.pages[page]

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0'
        }

        params = {
            'q': parse.quote_plus(query),
            'tbm':'isch',
            'start': page*10
        }

        response = requests.get(self.BASE_URL+'/search', params=params, headers=headers)
        if response.status_code != 200:
            return []

        data = response.content.decode()

        items = re.findall('\[\"https(.*?)\",',data, re.M|re.S)
        urls = []

        for i in items:
            if 'gstatic' in i:
                continue

            for j in ImageDownloader.ALLOWED_IMAGE_EXTENSIONS:
                if i[len(i) - len(j) - 1:] == '.' + j:
                    urls.append('https' + i)
                    break

        self.pages.append(urls)

        return urls
