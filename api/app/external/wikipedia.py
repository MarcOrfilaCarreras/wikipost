import wikipedia


class Scraper(object):
    def __init__(self):
        pass

    def scrape(self, url: str = None):
        if url is None:
            raise ValueError('You must provide the url to scrape')

        wikipedia.set_lang('es')

        name = url.split('/')[-1]
        page = wikipedia.page(name)

        title = page.title
        summary = wikipedia.summary(name, sentences=1)
        content = page.content

        return name, title, summary, content
