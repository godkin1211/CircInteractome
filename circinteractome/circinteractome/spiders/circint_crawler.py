# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy import Selector
from scrapy import Spider
from circinteractome.items import CircinteractomeItem
import pandas as pd
import re, time

def match_RBP(response):
    '''
    This function is used to check if a specific circRNA would be matched by any other RBPs. 
    :param response: Return value given by a web URL which received our request.
    :return: True or False.
    '''
    chktext = 'RNA-binding protein sites matching to circRNAs'
    chkpoint = response.xpath('//table[@width="100%"]/tr/th/font/text()').extract_first()
    if chkpoint != None and chkpoint == chktext:
        return True
    else:
        return False

def match_flankingRBP(response):
    '''
    This function is used to check if the flanking region of a specific circRNA would be matched by any other RBPs.
    :param response: Return value given by a web URL which received our request.
    :return: True or False.
    '''
    chktext = 'RNA-binding protein sites matching flanking regions of circRNA'
    chkpoint = response.xpath('//table[@width="600"]/tr/th[@colspan="2"]/font/text()').extract_first()
    if chkpoint != None and chkpoint == chktext:
        return True
    else:
        return False

class circintCrawler(Spider):
    name = 'circintCrawler'

    def start_requests(self):
        # Reading human circRNA list information
        human_circRNA_list = pd.read_csv('/home/nostalgie1211/Datasets/human_circRNA.csv')
        circRNAs = human_circRNA_list['circRNA ID'].tolist()
        # Define the url we want to scrape
        url = 'https://circinteractome.nia.nih.gov/bin/circsearchTest'
        for circrna in circRNAs:
            # Define the form-data to this URL according to POST method
            time.sleep(1)
            frmdata = 'gsymbol='+ circrna +'&gene=&tissue=test&submit=circRNA+Search'
            print('Start scraping {}'.format(circrna))
            yield Request(url=url, callback=self.parse, method="POST", body=str(frmdata))

    def parse(self, response):
        print('Get the CircRNA ID.....')
        circrna_matches = response.xpath('//table[@width="600"]/tr/td/a/font/text()').extract()
        crawlItems = CircinteractomeItem()
        crawlItems['circRNA'] = [i for i in circrna_matches if re.match(r'^hsa_circ_', i)][0]

        if match_RBP(response):
            pattern_rbps = r'data\.setCell\(\d+\, \d+\, \'(\w+)\''
            pattern_rbpsbs = r'data\.setCell\(\d+\, \d+\, (\d+)'
            rbps = response.xpath('//script[@type="text/javascript"]/text()').re(pattern_rbps)
            crawlItems['rbps'] = '|'.join(rbps)
            num_rbpsbs = response.xpath('//script[@type="text/javascript"]/text()').re(pattern_rbpsbs)
            crawlItems['num_rbpsbs'] = '|'.join(num_rbpsbs)
        else:
            crawlItems['rbps'] = "NA"
            crawlItems['num_rbpsbs'] = "NA"

        if match_flankingRBP(response):
            pattern_flanking_rbps = r'rbp=(\w+)'
            pattern_tags = r'^\d+$'
            flanking_rbps = response.xpath('//table[@width="600"]/tr/td[@bgcolor="#FFFFCC"]/a').re(pattern_flanking_rbps)
            crawlItems['flanking_rbps'] = '|'.join(flanking_rbps)
            num_tags = response.xpath('//table[@width="600"]/tr/td[@bgcolor="#FFFFCC"]/font[@size="-1"]/text()').re(pattern_tags)
            crawlItems['num_tags'] = '|'.join(num_tags)
        else:
            crawlItems['flanking_rbps'] = "NA"
            crawlItems['num_tags'] = "NA"

        return crawlItems
        #yield {
        #    "CircRNA": circrna,
        #    "RBPs": rbps,
        #    "Number_of_BindingSites": num_rbpsbs,
        #    "Match_flanking_region_RBPs": flanking_rbps,
        #    "Tags": num_tags
        #}

