# -*- coding: utf-8 -*-

# Scrapy settings for pricecompare project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'pricecompare'

SPIDER_MODULES = ['pricecompare.spiders']
NEWSPIDER_MODULE = 'pricecompare.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pricecompare (+http://www.yourdomain.com)'
LOG_LEVEL = 'DEBUG'
LOG_FILE = 'scrapy.log'