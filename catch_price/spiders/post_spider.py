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
        while True:
            for u in self.start_urls:
                yield scrapy.Request(u, headers=self.headers, cookies=self.cookies, callback=self.parse, dont_filter=True)

    def str2datetime(self, datetime_str):
        full_datetime_str = ""
        if len(datetime_str) == 5: # 13:31
            full_datetime_str = datetime.now().strftime('%Y-%m-%d ') + datetime_str
        elif len(datetime_str) == 11: # 09-25 20:28
            full_datetime_str = datetime.now().strftime('%Y-') + datetime_str
        return datetime.strptime(full_datetime_str, '%Y-%m-%d %H:%M')

    def datetime2str(self, dt):
        return dt.strftime('%Y-%m-%d %H:%M')

    def parse(self, response):
        if response.url not in self.post_datetime_dic:
            self.post_datetime_dic[response.url] = datetime.now()

        datetime_str = response.css('.feed-block-extras').xpath('text()').extract_first().strip()
        new_datetime = self.str2datetime(datetime_str)
        print(new_datetime)
        print(self.post_datetime_dic[response.url])
        print("new_datetime: {0}, current_datetime: {1}".format(self.datetime2str(new_datetime), self.datetime2str(self.post_datetime_dic[response.url])))
        if new_datetime > self.post_datetime_dic[response.url]:
            self.post_datetime_dic[response.url] = new_datetime
            logging.warning('{0}: new price!!!!!!!'.format(response.status))
            print('{0}: new price!!!!!!!'.format(response.status))
            SendEmail().send(self.get_name_by_url(response.url), response.url)
            logging.info('sent email')
            print('sent email')
        else:
            logging.info('{0}: same...'.format(response.status))
            print('{0}: same...'.format(response.status))

        # Tell the admin I'm fine
        if datetime.now().hour == 6 and datetime.now().minute < 20:
            SendEmail().send("I'm the smzdm spider, and I just want to tell you I'm fine, take care.", '')

    def get_name_by_url(self, url):
        dic = {
            self.muh_milk: "MUH 甘蒂牧场 全脂纯牛奶 1L*12盒",
            self.finish: "亮碟洗碗粉"
        }
        return dic[url]
