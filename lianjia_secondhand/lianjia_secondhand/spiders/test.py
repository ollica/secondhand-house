from scrapy import Spider

class MySpider(Spider):
    name = 'my_spider'
    
    start_urls = ['https://su.lianjia.com/ershoufang']
    
    def parse(self, response):
        page = response.xpath('(//div[@class="page-box house-lst-page-box"]//a)[last()-1]/@data-page').get()
        self.logger.info(page)
