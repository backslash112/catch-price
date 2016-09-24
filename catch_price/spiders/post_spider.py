#!/usr/bin/python
#coding:utf-8

import scrapy
from catch_price.items import PostItem
from catch_price.settings import *
from datetime import datetime
from catch_price.send_email import SendEmail
import logging

class PostSpider(scrapy.Spider):
    name = "post"
    muh_milk = "http://search.smzdm.com/?c=home&s=muh+1L"
    finish = "http://search.smzdm.com/?c=home&s=Finish%E6%B4%97%E7%A2%97%E7%B2%89"
    start_urls = [
        muh_milk,
        finish
    ]
    post_datetime_dic = {}
    headers = HEADERS
    cookies = COOKIES

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, headers=self.headers, cookies=self.cookies, callback=self.parse, dont_filter=True)

    def parse(self, response):
        if response.url not in self.post_datetime_dic:
            self.post_datetime_dic[response.url] = datetime.strptime('01-01 01:01', '%m-%d %H:%M')

        datetime_str = response.css('.feed-block-extras').xpath('text()').extract_first().strip()
        new_datetime = datetime.strptime(datetime_str, '%m-%d %H:%M')

        if new_datetime > self.post_datetime_dic[response.url]:
            self.post_datetime_dic[response.url] = new_datetime
            logging.warning('{0}: new price!!!!!!!'.format(response.status))
            SendEmail().send(self.get_name_by_url(response.url), response.url)
            logging.info('sent email')
        else:
            logging.info('{0}: same...'.format(response.status))

        for u in self.start_urls:
            yield scrapy.Request(u, headers=self.headers, cookies=self.cookies, callback=self.parse, dont_filter=True)

    def get_name_by_url(self, url):
        dic = {
            self.muh_milk: "MUH 甘蒂牧场 全脂纯牛奶 1L*12盒",
            self.finish: "亮碟洗碗粉"
        }
        return dic[url]
