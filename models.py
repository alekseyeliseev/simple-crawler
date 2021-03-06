import requests
from bs4 import BeautifulSoup
import re
from utils import preproc_line


class Website:

    def __init__(self, name, url, targetPattern, absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.targetPattern = targetPattern
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag


class Content:

    def __init__(self, url, title, body, body_processed):
        self.url = url
        self.title = title
        self.body = body
        self.body_processed = body_processed


class Crawler:
    def __init__(self, site):
        self.site = site
        self.visited = []
        self.results = []

    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        selectedElems = pageObj.select(selector)

        if selectedElems is not None and len(selectedElems) > 0:
            return selectedElems[0].get_text()
        return ''

    def parse(self, url):
        bs = self.getPage(url)
        if bs is not None:
            # убирает последний пробел в заголовке
            title = self.safeGet(bs, self.site.titleTag).rstrip()
            body = self.safeGet(bs, self.site.bodyTag)
            if title != '' and body != '':
                body_processed = preproc_line(body)
                content = Content(url, title, body, body_processed)
                self.results.append(content)

    def crawl(self):
        """
        Получение страниц, начиная со стартовой
        """
        bs = self.getPage(self.site.url)
        if bs is None:
            return self.results
        targetPages = bs.findAll('a', href=re.compile(self.site.targetPattern))
        for targetPage in targetPages:
            targetPage = targetPage.attrs['href']
            if targetPage not in self.visited:
                self.visited.append(targetPage)
                if not self.site.absoluteUrl:
                    targetPage = '{}{}'.format(self.site.url, targetPage)
                self.parse(targetPage)
        return self.results
