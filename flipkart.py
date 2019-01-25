# -*- coding: utf-8 -*-
import scrapy,os,time,re
from math import ceil
from pricecompare.items import PricecompareItem
from scrapy.http.request import Request

class FlipkartSpider(scrapy.Spider):
    name = "flipkart"
    allowed_domains = ["flipkart.com"]
    start_urls = (
                    'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?p[]=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock&sid=tyy%2C4io&filterNone=true&view=smartphones~type&ajax=true&_=1441788713785',
                 )
    #'http://www.flipkart.com/mobiles/smartphones~type/pr?p[]=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock&sid=tyy%2C4io&filterNone=true',
    #'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?p[]=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock&sid=tyy%2C4io&filterNone=true&view=smartphones~type&ajax=true&_=1441788713785'

    def makePaginatedUrls(self, url, totalProducts, onePageProducts):
        urls = []
        noOfPages = int(ceil(totalProducts / onePageProducts))
        for i in range(1, noOfPages + 1):
            page_url = url + '&start=' + str((i - 1) * 20+1)
            urls.append(page_url)
        return urls

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

    def getHtmlData(self,html_text=None):
        return

    def parsePaginated(self, response):

        blocks = response.xpath(".//div[@class='gd-col gu3']")

        if len(blocks)>0:

            for block in blocks:

                product = PricecompareItem()

                try:
                    product['price'] = self.extractPrice( block.xpath(".//div[@class='pu-final']/span/text()").extract()[0] )
                except:
                    product['price'] = ''
                    pass

                try:
                    product['title'] = self.cleanQueryStringForSolr(block.xpath(".//div[contains(@class,'pu-title')]/a/@title").extract()[0])
                except:
                    product['title'] = ''
                    pass

                try:
                    product['prod_img'] = block.xpath(".//div[@class='pu-visual-section']//img/@data-src").extract()[0]
                except:
                    product['prod_img'] = ''
                    pass

                try:
                    product['website_prod_id'] = block.xpath(".//div[@class='pu-visual-section']//a/@data-pid").extract()[0]
                except:
                    product['website_prod_id'] = ''
                    pass

                try:
                    product['website_prod_url'] = block.xpath(".//div[contains(@class,'pu-title')]/a/@href").extract()[0]
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

        for url in self.makePaginatedUrls(url=response.url, totalProducts=2091,onePageProducts=20):

            time.sleep(0.5)

            print "Fetching : "+url

            request = Request(url, callback=self.parsePaginated)

            yield request

