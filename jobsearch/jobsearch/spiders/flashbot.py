#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 09:03:45 2020

@author: randon
"""

import scrapy
from scrapy import Request
from pymongo import MongoClient


class FlashbotSpider(scrapy.Spider):
    name = 'flashbot'
    allowed_domains = ['rss.jobsearch.monster.com']

    start_urls = ['http://rss.jobsearch.monster.com/rssquery.ashx?q={query}']


    thesaurus = ["machine learning", "machine", "big data", "big", "data", "python", "sql", "ia", "nosql"]

    LOG_LEVEL = "INFO"

    def parse(self, response):

        # We stat with this url
        url = self.start_urls[0]

        # Build and send a request for each word of the thesaurus
        for query in self.thesaurus:
            target = url.format(query=query)
            print("fetching the URL: %s" % target)
            if target.startswith("file://"):
                r = Request(target, callback=self.scrapit, dont_filter=False)
            else:
                r = Request(target, callback=self.scrapit)
            r.meta['query'] = query
            yield r

    def scrapit(self, response):
        query = response.meta["query"]
        
        client = MongoClient("localhost", 27017)
        db = client["jobsearchengine"]
        collection = db["testjob"]
        
        # Base item with query used to this response
        item = {"query": query}
        print(query, response)

        # Scrap the data
        for doc in response.xpath("//item"):
            item["title"] = doc.xpath("title/text()").extract_first()
            item["description"] = doc.xpath("description/text()").extract_first()
            item["link"] = doc.xpath("link/text()").extract_first()
            item["pubDate"] = doc.xpath("pubDate/text()").extract_first()
            item["guid"] = doc.xpath("guid/text()").extract_first()
            #pprint(item, indent=2)
            print("item scraped:", item["title"])
            yield item