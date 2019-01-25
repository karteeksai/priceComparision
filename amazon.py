# -*- coding: utf-8 -*-
import scrapy,os,time,re
from math import ceil
from pricecompare.items import PricecompareItem
from scrapy.http.request import Request


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.in"]
    start_urls = (
        'http://www.amazon.in/smartphones-basic-mobiles/b?ie=UTF8&node=1389432031',
    )
    user_agent = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'

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
        noOfPages = int(ceil(totalProducts / onePageProducts))
        for i in range(1, noOfPages + 1):
            urls.append(url + '&page=' + str(i))
        return urls

    def parsePaginated(self, response):

        blocks = response.xpath(".//*[contains(@id,'result_')]")

        if len(blocks)>0:

            for block in blocks:

                product = PricecompareItem()

                try:
                    product['price'] = self.extractPrice( block.xpath(".//div/a/span[@class='bld lrg red']/text()").extract()[1] )
                except:
                    product['price'] = ''
                    pass

                try:
                    product['title'] = self.cleanQueryStringForSolr(block.xpath(".//a/span[@class='lrg bold']/text()").extract()[0])
                except:
                    product['title'] = ''
                    pass

                try:
                    product['prod_img'] = block.xpath(".//div[@class='imageBox']/img/@src").extract()[0]
                except:
                    product['prod_img'] = ''
                    pass

                try:
                    product['website_prod_id'] = block.xpath("./@name").extract()[0]
                except:
                    product['website_prod_id'] = ''
                    pass

                try:
                    product['website_prod_url'] = block.xpath(".//h3[@class='newaps']/a/@href").extract()[0]
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

        for url in self.makePaginatedUrls(url=response.url, totalProducts=1345,onePageProducts=24):

            #time.sleep(0.5)

            print "Fetching : "+url

            request = Request(url, callback=self.parsePaginated)

            yield request


