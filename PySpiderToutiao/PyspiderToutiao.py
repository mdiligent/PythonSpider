#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-02-07 11:22:20
# Project: toutiao

from pyspider.libs.base_handler import *
import requests
from urllib.parse import urlencode
from requests import codes
import os
from hashlib import md5
from multiprocessing.pool import Pool
import re

default_headers = {
    'cookie': 'tt_webid=6667396596445660679; csrftoken=3a212e0c06e7821650315a4fecf47ac9; tt_webid=6667396596445660679; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16b846003e03d7-0dd00a2eb5ea11-353166-1fa400-16b846003e1566; CNZZDATA1259612802=2077267981-1561291030-https%253A%252F%252Fwww.baidu.com%252F%7C1561361230; __tasessionId=4vm71cznd1561363013083; sso_uid_tt=47d6f9788277e4e071f3825a3c36a294; toutiao_sso_user=e02fd616c83dff880adda691cd201aaa; login_flag=6859a0b8ffdb01687b00fe96bbeeba6e; sessionid=21f852358a845d783bdbe1236c9b385b; uid_tt=d40499ec45187c2d411cb7bf656330730d8c15a783bb6284da0f73104cd300a2; sid_tt=21f852358a845d783bdbe1236c9b385b; sid_guard="21f852358a845d783bdbe1236c9b385b|1561363028|15552000|Sat\054 21-Dec-2019 07:57:08 GMT"; s_v_web_id=6f40e192e0bdeb62ff50fca2bcdf2944',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
}


class Handler(BaseHandler):
    crawl_config = {
        'headers': default_headers,
        'validate_cert': False,
    }
    offset = 0
    num = 0
    #网页url提交的参数中只有起下拉加载更多的offset是变化的
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset * 20,
        'format': 'json',
        'keyword': '插画',
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
    }
    base_url = 'https://www.toutiao.com/api/search/content/?'
    url = base_url + urlencode(params)

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.url, callback=self.json_parser)

    @config(age=10 * 24 * 60 * 60)
    def json_parser(self, response):
        images = []
        for item in response.json['data']:
            if "image_list" in item:
                images.extend(item["image_list"])#将图片url整合到一个列表中
                titles = item['title']

        for url in images:
            #根据获得的小图片url和网站规则，替换成大图url
            origin_image = re.sub("list.*?pgc-image", "large/pgc-image", url['url'])
            self.crawl(origin_image, callback=self.download_image, save={'titles': titles})
        #加载并爬取10次数据
        if self.offset < 10:
            self.offset += 1
            next = self.base_url + urlencode(self.params)
            self.crawl(next, callback=self.json_parser)

    def download_image(self, response):
        title = response.save['titles']
        img_path = 'F:\\img' + os.path.sep + title #指定保存到F盘，可自由选择
        if not os.path.exists(img_path):
            os.makedirs(img_path)

        resp = response
        file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(
            file_name=md5(resp.content).hexdigest(),
            file_suffix='jpg')
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(resp.content)
                return('Downloaded image path is %s' % file_path)
        else:
            return('Already Downloaded', file_path)



















