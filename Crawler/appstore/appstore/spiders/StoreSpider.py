import urllib
import scrapy
import scrapy.spiders as ss
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from bs4 import BeautifulSoup
from appstore.items import AppstoreItem


class StoreSpider(ss.CrawlSpider):
    name = "store"
    start_urls = ['https://www.microsoft.com/en-in/store/top-free/apps/pc',
                  'https://www.microsoft.com/en-in/store/top-free/games/mobile',
                  'https://www.microsoft.com/en-in/store/top-free/games/pc',
                  'https://www.microsoft.com/en-in/store/top-free/games/xbox',
                  'https://www.microsoft.com/en-in/store/top-free/apps/mobile']
    rules = (
        ss.Rule(LinkExtractor(allow=(), deny=(".*-1"), restrict_xpaths=(
            "//a[contains(@aria-label,'next page')]")), callback='parse_item', follow=True),
    )
    custom_settings = {
        'ITEM_PIPELINES': {
            'appstore.pipelines.AppstorePipeline': 300
        }
    }
    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        #print(response.url)
        selected = Selector(response=response).xpath(
            '//div[contains(@class, "c-group f-wrap-items context-list-page")]')
        sections = selected.xpath(
            "//section[contains(@class,'m-product-placement-item f-size-medium context-app')]")
        # print(len(sections))
        for section in sections:
            soup = BeautifulSoup(section.extract(), 'html.parser')
            try:
                item = AppstoreItem()
                item['name'] = soup.h3.text
                item['rating'] = soup.find(
                    'span', {'itemprop': 'ratingValue'}).text
                item['url'] = urllib.parse.urljoin(
                    response.url, soup.find('a')['href'])
                yield item
            except:
                pass