import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Request
from douban.items import DoubanMovieItem
from douban.dns_cache import _setDNSCache
from scrapy.http import FormRequest
from faker import Factory
import numpy as np
f = Factory.create()

class DoubanMovieSpider(scrapy.Spider):

    name = 'douban-movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/']

    custom_settings = {  # 自定义该spider的pipeline输出
        'ITEM_PIPELINES': {
            'douban.pipelines.MovieItemPipeline': 1,
        }
    }

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
        #self.headers['Host'] = "movie.douban.com"
        movie_id = np.loadtxt('config/movie_id.out', dtype='i').tolist()  # Top250
        i = 0
        for mid in movie_id:
            if (i >= 2):
                break
            i += 1
            yield scrapy.Request(url='https://movie.douban.com/subject/%s/' % mid,
                                 meta={'cookiejar': response.meta['cookiejar']},
                                 callback=self.parse_movie)

    def parse_movie(self, response):
        print(response.status)
        movie_item = DoubanMovieItem()
        # movie id
        movie_item['movie_id'] = response.xpath('.//li/span[@class="rec"]/@id').extract()
        # movie title
        movie_item['movie_title'] = response.xpath('.//h1/span[@property="v:itemreviewed"]/text()').extract()
        # release_date
        movie_item['release_date'] = response.xpath('.//h1/span[@class="year"]/text()').extract()
        # 导演
        movie_item['directedBy'] = response.xpath('.//a[@rel="v:directedBy"]/text()').extract()
        # 电影主演
        movie_item['starring'] = response.xpath('.//a[@rel="v:starring"]/text()').extract()
        # 电影类别
        movie_item['genre'] = response.xpath('.//span[@property="v:genre"]/text()').extract()
        # 电影时长
        movie_item['runtime'] = response.xpath('.//span[@property="v:runtime"]/text()').extract()
        #电影的国别和语言
        temp = response.xpath('.//div[@id="info"]/text()').extract()
        movie_item['country'] = [p for p in temp if (p.strip() != '') & (p.strip() != '/')][0].strip()
        movie_item['language'] = [p for p in temp if (p.strip() != '') & (p.strip() != '/')][1].strip()
        # 电影的评分
        movie_item['rating_num'] = response.xpath('.//strong[@class="ll rating_num"]/text()').extract()
        # 评分的人数
        movie_item['vote_num'] = response.xpath('.//span[@property="v:votes"]/text()').extract()
        # 电影1-5星的百分比
        movie_item['rating_per_stars5'] = response.xpath('.//span[@class="rating_per"]/text()').extract()[0].strip()
        movie_item['rating_per_stars4'] = response.xpath('.//span[@class="rating_per"]/text()').extract()[1].strip()
        movie_item['rating_per_stars3'] = response.xpath('.//span[@class="rating_per"]/text()').extract()[2].strip()
        movie_item['rating_per_stars2'] = response.xpath('.//span[@class="rating_per"]/text()').extract()[3].strip()
        movie_item['rating_per_stars1'] = response.xpath('.//span[@class="rating_per"]/text()').extract()[4].strip()
        #电影的剧情简介
        intro = response.xpath('.//span[@class="all hidden"]/text()').extract()
        if len(intro):
            movie_item['intro'] = intro
        else:
            movie_item['intro'] = response.xpath('.//span[@property="v:summary"]/text()').extract()
        # 电影的短评数
        movie_item['comment_num'] = response.xpath('.//div[@class="mod-hd"]/h2/span/a/text()').extract()[0].strip()
        # 电影的提问数
        movie_item['question_num'] = response.xpath('.//div[@class="mod-hd"]/h2/span/a/text()').extract()[1].strip()

        #最后输出
        print(movie_item)
        yield movie_item


