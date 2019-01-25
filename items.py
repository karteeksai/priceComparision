# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PricecompareItem(scrapy.Item):

    # define the fields for your item here like:

    price           = scrapy.Field()

    title           = scrapy.Field()

    prod_img        = scrapy.Field()

    website_prod_id = scrapy.Field()

    website_prod_url= scrapy.Field()

    category        = scrapy.Field()

    start_url       = scrapy.Field()

    '''
        name = scrapy.Field()

        name = scrapy.Field()

        name = scrapy.Field()

        name = scrapy.Field()

        name = scrapy.Field()

        name = scrapy.Field()
    '''

    pass
