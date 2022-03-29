import requests
from abc import ABC, abstractmethod
from parsercrawler import JobsoffersParser
from bs4 import BeautifulSoup
from storage import MongoDataBase
from config import BASE_LINK, STORAGE_TYPE
from adv import get

class BaseCrawler(ABC):
    def __init__(self):
        self.storage = self.__set_storage()

    @staticmethod
    def __set_storage():
        if STORAGE_TYPE == 'mongo':
            return MongoDataBase()


    @abstractmethod
    def start(self, store=False):
        pass

    @abstractmethod
    def store(self, data, filename):
        pass


class LinkCrawler(BaseCrawler):
    def __init__(self, link=BASE_LINK):
        super().__init__()
        self.link = link


    @staticmethod
    def find_links(html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        links = soup.find_all('a', attrs={'class': 'chakra-link css-f4h6uy'})
        return links

    def start_crawl_pages(self, url):
        jobs_list = list()
        crawl = True
        pages = 1
        while crawl:
            response = get(url + str(pages))
            if response is None:
                crawl = False
            jobs_links = self.find_links(response)
            jobs_list.extend(jobs_links)
            pages += 1
            crawl = bool(len(jobs_links))

        return jobs_list

    def start(self, store=False):
        jobs_list = list()
        job_link = self.start_crawl_pages(self.link)
        for li in job_link:
            jobs_list.extend(li.get('href'))
            if store:
                self.store({"url": f"https://quera.ir/{li.get('href')}"}, "jobs_links")

        print(f"total : {len(jobs_list)}")
        return jobs_list

    def store(self, data, *args):
        self.storage.store(data, "jobs_links")


class DataCrawler(BaseCrawler):

    def __init__(self):
        super().__init__()
        self.links = self.__load_links()
        self.pars = JobsoffersParser()

    def __load_links(self):
        return self.storage.load()

    def start(self, store=False):
        for link in self.links:
            response = get(link['url'])
            if response is None:
                raise requests.HTTPError
            data = self.pars.parser(response)
            if store:
                self.store(data, data.get('Essential_skill', 'sample'))

    def store(self, data, filename):
        self.storage.store(data, "jobs_info")
