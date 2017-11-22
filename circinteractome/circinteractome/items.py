# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item
from scrapy import Field

class CircinteractomeItem(Item):
    # define the fields for your item here like:
    circRNA = Field()
    rbps = Field()
    num_rbpsbs = Field()
    flanking_rbps = Field()
    num_tags = Field()

class circRNA2miRNAItem(Item):
    circRNA = Field()
    miRNAs = Field()
    numSites = Field()
