import sys
from crawler import LinkCrawler, DataCrawler

if __name__ == "__main__":
    switch = sys.argv[1]
    if switch == 'Extract_pages':
        crawler = DataCrawler()
        crawler.start(store=True)
    elif switch == 'Link_finders':
        crawler = LinkCrawler()
        crawler.start(store=True)
    else:
        print('please pass switch after "main.py" --> "Link_finders" | "Extract_pages". ')
