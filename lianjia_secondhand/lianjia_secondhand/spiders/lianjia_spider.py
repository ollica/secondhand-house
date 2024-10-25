import re
import pymysql
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import LianjiaSecondhandItem
from ..data_cleaner import clean_data
from fake_useragent import UserAgent
from scrapy import Request
import time
import random
class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['su.lianjia.com']
    start_urls = ['https://su.lianjia.com/ershoufang/']
    total_items = 0
    # max_items = 100000000000
    user_agent = UserAgent().random
    
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers={'User-Agent': self.user_agent})
    
    def parse(self, response):
        div_element = response.xpath('//div[@data-role="ditiefang"]') 
        if div_element:
            links = div_element.xpath('.//a/@href').extract()
            # print("!!!!!!!!!!" + str(links))
            for link in links:
                full_url = response.urljoin(link)
                yield Request(url=full_url, callback=self.parse_url, 
                                     headers={'User-Agent': self.user_agent})
    
    def parse_url(self, response):
        div_element = response.xpath('//div[@data-role="ditiefang"]/div[2]') 
        if div_element:
            links = div_element.xpath('.//a/@href').extract()
            # print("##########" + str(links))
            for link in links:
                full_url = response.urljoin(link)
                yield Request(url=full_url, callback=self.parse_final, 
                              meta={'url': full_url, 'url_num': 1, 'house_cnt': 0},
                              headers={'User-Agent': self.user_agent})
            
    def parse_final(self, response):
        url = response.meta['url']
        url_num = response.meta['url_num']
        house_cnt = response.meta['house_cnt']
        if response.status == 200:
            # URL exists
            print(f"URL {url} exists and returned status code 200", ":::::::",url_num)
            # Further processing logic here
            #next_url = f"{url_back}pg{url_num+1}"
            # Further processing logic here
            """ yield Request(url= next_url, callback=self.parse_final, 
                              meta={'url': url_back, 'url_num': url_num + 1}, 
                              headers={'User-Agent': self.user_agent})     """
        elif response.status >= 300 and response.status < 400:
            # URL was redirected
            print(f"URL {url} was redirected with status code {response.status}")
            # Further processing logic for redirection
            return
        else:
            # URL does not exist or encountered an error
            print(f"URL {url} does not exist or encountered an error with status code {response.status}")
            return
            
        house_list = response.xpath('//ul[@class="sellListContent"]/li')   
        house_amount = int(response.xpath('//div[@class="resultDes clear"]/h2/span/text()').get()) 
        print("house_amount:", house_amount)
        for house in house_list:
            """ if self.total_items >= self.max_items:
                break """
            item = LianjiaSecondhandItem()
            item['title'] = house.xpath('.//div[@class="title"]/a/text()').get()
            item['total_price'] = house.xpath('.//div[@class="totalPrice totalPrice2"]/span/text()').get()
            item['unit_price'] = house.xpath('.//div[@class="unitPrice"]/@data-price').get()
            item['info'] = house.xpath('.//div[@class="houseInfo"]/text()').get()
            house_cnt += 1
            href = house.xpath('.//div[@class="title"]/a/@href').get()
            yield Request(url=response.urljoin(href), callback=self.parse_location,
                          meta={'item': item}, headers={'User-Agent': self.user_agent})
            self.total_items += 1
            if self.total_items % 3000 == 0:
                print(f"Pausing spider for 180 second after every 3000 requests...")
                time.sleep(1)
            #time.sleep(random.randint(0,3))
        if house_cnt < house_amount:      # self.total_items < self.max_items:
            url_num += 1
            next_page_url = url + "pg" + str(url_num)
            yield scrapy.Request(next_page_url, callback=self.parse_final,
                                 meta={'url': url, 'url_num' : url_num, 'house_cnt': house_cnt},   # check url
                                 headers={'User-Agent': self.user_agent})
                
    """ def parse_next_page(self, response):
        url = response.meta.get('url')
        url_num = response.meta.get('url_num')
        print("000000000000" + str(url),"::::",url_num)
        url_back = url[:-3]
        if response.status == 200:
            # URL exists
            print(f"URL {url} exists and returned status code 200")
            # Further processing logic here
            next_url = f"{url_back}pg{url_num+1}"
            # Further processing logic here
            yield Request(url= next_url, callback=self.parse_final, 
                              meta={'url': url_back, 'url_num': url_num + 1}, 
                              headers={'User-Agent': self.user_agent})    
        elif response.status >= 300 and response.status < 400:
            # URL was redirected
            print(f"URL {url} was redirected with status code {response.status}")
            # Further processing logic for redirection
        else:
            # URL does not exist or encountered an error
            print(f"URL {url} does not exist or encountered an error with status code {response.status}")
     """
    # def parse_house(self, response):
        
    def parse_location(self, response):
        item = response.meta['item']
        location_info = response.xpath('//div[@class="areaName"]/span[@class="info"]/a/text()').get()
        item['location'] = location_info
        yield item
        
        """ yield from self.output_item(item)
        
    def output_item(self, item):
        # Clean the data
        cleaned_title, cleaned_price, cleaned_info, cleaned_location = clean_data(item)
        cleaned_data = {
            'title': cleaned_title,
            'price': cleaned_price,
            'info': cleaned_info,
            'location': cleaned_location
        }
        yield cleaned_data """
            
        
        