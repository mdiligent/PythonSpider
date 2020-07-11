import scrapy
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Request
from douban.items import DoubanMovieItem
from douban.dns_cache import _setDNSCache
from scrapy.http import FormRequest
from faker import Factory
import numpy as np
f = Factory.create()

class MovieCommentsSpider(scrapy.Spider):
    name = 'movie-comments'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']

    base_url = 'https://movie.douban.com/subject/1652592/comments'

    def start_requests(self):
        return [Request(url='https://movie.douban.com',
                        meta={'cookiejar': 1},
                        callback=self.post_login)]

    def post_login(self, response):
        return FormRequest(
            url='https://accounts.douban.com/j/mobile/login/basic',
            method='POST',
            formdata={
                'ck': '',
                'name': '',#手机号/邮箱
                'password': '',#密码
                'remember': 'false',
                'ticket': ''
            },
            meta={'cookiejar': response.meta['cookiejar']},
            dont_filter=True,
            callback=self.after_login
        )

    def after_login(self, response):
        _setDNSCache()
        # print(response.status)
        # self.headers['Host'] = "movie.douban.com"
        movie_id = np.loadtxt('config/movie_id.out', dtype='i').tolist()  # Top250
        i = 0
        for mid in movie_id:
            if (i >= 2):
                break
            i += 1
            yield scrapy.Request(url='https://movie.douban.com/subject/%s/' % mid,
                                 meta={'cookiejar': response.meta['cookiejar']},
                                 callback=self.parse_comments)
