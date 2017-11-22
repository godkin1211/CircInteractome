# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy import Selector
from scrapy import Spider
from circinteractome.items import circRNA2miRNAItem
import pandas as pd
import re, time

class circ2mirCrawler(Spider):
    name = 'circ2mirCrawler'

    def start_requests(self):
        # Reading human circRNA list information
        human_circRNA_list = pd.read_csv('/Users/nostalgie1211/Google 雲端硬碟/CodingGround/Python_codes/Scrapy_test/circinteractome/human_circRNA.csv')
        circRNAs = human_circRNA_list['circRNA ID'].tolist()
        # Define the url we want to scrape
        url = 'https://circinteractome.nia.nih.gov/bin/mirnasearch'
        for circrna in circRNAs[33000:]:
            # Define the form-data to this URL according to POST method
            time.sleep(1)
            frmdata = 'gcircrna='+ circrna +'&gsymbol=&submit=miRNA+Target+Search'
            print('Start scraping {}'.format(circrna))
            request = Request(url=url, callback=self.parse, method="POST", body=str(frmdata))
            request.meta['circrna'] = circrna
            yield request

    def parse(self, response):
        crawlItems = circRNA2miRNAItem()
        crawlItems['circRNA'] = response.meta['circrna']
        pattern_miRNA = r'data\.setCell\(\d+\, \d+\, \'(.*)\'\);'
        pattern_mir_Sites = r'data\.setCell\(\d+\, \d+\, (\d+)\);'
        miRNAs = response.xpath('//script[@type="text/javascript"]/text()').re(pattern_miRNA)
        crawlItems['miRNAs'] = miRNAs
        miRNA_sites = response.xpath('//script[@type="text/javascript"]/text()').re(pattern_mir_Sites)
        crawlItems['numSites'] = miRNA_sites
        print('CircRNA {} has been fetched!'.format(response.meta['circrna']))
        return crawlItems
