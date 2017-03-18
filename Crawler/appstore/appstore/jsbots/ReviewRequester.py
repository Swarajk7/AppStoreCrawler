import requests


class ReviewRequester:
    def __init__(self):
        self.reviews = []
        self.start = 0
        self.skip = 25
        self.productId = None
        self.result = []

    def setProductId(self, productId):
        self.productId = productId

    def getUrl(self, value):
        urlTemplate = "https://www.microsoft.com/en-in/store/webapi/reviews?language=en-in&market=IN&productid={0}&channelid=reviews&skipItems={1}&pageSize={2}"
        url = urlTemplate.format(self.productId, value, self.skip)
        return url

    def crawlReviews(self):
        if self.productId:
            headers = requests.utils.default_headers()
            headers.update({'User-Agent': 'Mozilla/5.0'})
            current = self.start
            count = 0
            while True:
                try:
                    url = self.getUrl(current)
                    items = requests.get(url, headers=headers).json()
                    if len(items['Items']) == 0:
                        break
                    count += 1
                    current += self.skip
                    self.result += items['Items']
                except:
                    print('Failed' + self.productId)
            print(count)

    def processAndGetResult(self):
        if len(self.result) == 0:
            return

        def filter(z):
            try:
                review_ = {}
                review_['ReviewId'] = z['ReviewId']
                review_['ReviewText'] = z['ReviewText']
                review_['UserName'] = z['UserName']
                review_['Rating'] = z['Rating']['AverageRating']
                review_['Title'] = z['Title']
            except Exception as ex:
                raise ex
            return review_
        return list(map(filter, self.result))

    def getResult(self):
        return self.result
