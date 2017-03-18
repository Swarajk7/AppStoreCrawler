import time
import json
import scrapy.spiders as ss
from bs4 import BeautifulSoup
from appstore.jsbots.ReviewRequester import ReviewRequester
from appstore.items import AppItem


class AppSpider(ss.CrawlSpider):
    name = 'app'
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {
            'appstore.pipelines.AppPipeline': 300
        }
    }
    with open('items.json') as data_file:
        data = json.load(data_file)
    for datum in data:
        start_urls.append(datum['url'])

    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        ratings_div = response.xpath("//div[@class='m-histogram']")
        soup = BeautifulSoup(ratings_div[0].extract(), 'html.parser')
        li_list = soup.ul.find_all('li')
        rating_list = []
        item = AppItem()
        for li in li_list:
            try:
                rating = {}
                stars = li.find('span', {'class': 'x-screen-reader'}).text
                rat = li.find_all('span')[-1].text
                rating['stars'] = stars
                rating['count'] = rat
                rating_list.append(rating)
            except:
                pass
        print(rating_list)
        product_id = response.url.split('/')[-1]
        requestor = ReviewRequester()
        requestor.setProductId(product_id)
        requestor.crawlReviews()
        reviews = requestor.processAndGetResult()
        item['product_id'] = product_id
        item['ratings'] = rating_list
        item['reviews'] = reviews
        category_p = response.xpath("//p[@id='category-toggle-target']")
        soup = BeautifulSoup(category_p[0].extract(), 'html.parser')
        item['category'] = soup.span.text.strip()
        description_p = response.xpath("//p[@id='product-description']")
        soup = BeautifulSoup(description_p[0].extract(), 'html.parser')
        item['description'] = soup.text.replace(
            "\r\n", " ").replace("\n", " ").strip()
        title_h1 = response.xpath("//h1[@id='page-title']")
        soup = BeautifulSoup(title_h1[0].extract(), 'html.parser')
        item['name'] = soup.text.strip()
        yield item
        time.sleep(5)
