# -*- coding: utf-8 -*-
import scrapy,os,time,re
from math import ceil
from pricecompare.items import PricecompareItem
from scrapy.http.request import Request

class SnapdealSpider(scrapy.Spider):
    name = "snapdeal"
    allowed_domains = ["snapdeal.com"]
    start_urls = (
        'http://www.snapdeal.com/acors/json/product/get/search/175/0/20?q=&sort=plrty&keyword=&clickSrc=&viewType=List&lang=en&snr=false',
    )

    def extractPrice(self,str):
        try:
            matches = re.findall(r'[\d+\,]+', str)
            if matches:
                matches = [float(match.replace(',', '')) for match in matches]
                return matches[0]
        except:
            print 'exception in price extraction'
            pass
        return str

    def cleanQueryStringForSolr(self, str):
        if isinstance(str,float):
            return str
        if isinstance(str,int):
            return str
        str = str.strip()
        str = str.replace("'","")
        str = re.sub("[^0-9a-zA-Z]+", ' ', str)
        str = re.sub('\s+', ' ', str)
        return str

    def makePaginatedUrls(self, url, totalProducts, onePageProducts):
        urls = []
        totalProducts=int(totalProducts)
        onePageProducts=int(onePageProducts)
        noOfPages = int(ceil(totalProducts / onePageProducts))
        for i in range(1, noOfPages + 1):
            urls.append(url.replace("/0/","/"+str(onePageProducts*i)+"/"))
        return urls

    def parsePaginated(self, response):

        blocks = response.xpath(".//div[@class='product_grid_box']")

        if len(blocks)>0:

            for block in blocks:

                product = PricecompareItem()

                try:
                    product['price'] = self.extractPrice( block.xpath(".//div[@class='product-price']/div[1]/p/text()").extract()[0] )

                except:
                    product['price'] = ''
                    pass

                try:
                    product['title'] = self.cleanQueryStringForSolr(block.xpath(".//div[@class='product-title']/a/text()").extract()[0])
                except:
                    product['title'] = ''
                    pass

                try:
                    product['prod_img'] = block.xpath(".//img[@class='gridViewImage']/@src").extract()[0]
                except:
                    product['prod_img'] = ''
                    pass

                try:
                    product['website_prod_id'] = block.xpath(".//div[@class='outerImg']/div/a/@pogid").extract()[0]
                except:
                    product['website_prod_id'] = ''
                    pass

                try:
                    product['website_prod_url'] = block.xpath(".//div[@class='product-title']/a/@href").extract()[0]
                except:
                    product['website_prod_url'] = ''
                    pass

                product['category'] = "Mobiles"

                product['start_url'] = response.url

                print product

                yield product
        else:
            print '0 products found'

    def parse(self, response):

        for url in self.makePaginatedUrls(url=response.url, totalProducts=8000,onePageProducts=20):
            #time.sleep(2)
            print "Fetching : "+url
            request = Request(url, callback=self.parsePaginated)
            yield request

