# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanMovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_id = scrapy.Field()  # 电影的唯一ID
    movie_title = scrapy.Field()  # 电影名字
    release_date = scrapy.Field()  # 电影发布日期
    directedBy = scrapy.Field()  # 电影导演
    starring = scrapy.Field()  # 电影主演
    genre = scrapy.Field()  # 电影类型
    runtime = scrapy.Field()  # 电影时长
    country = scrapy.Field()  # 电影的国别
    language = scrapy.Field()  # 电影的语言
    rating_num = scrapy.Field()  # 电影总评分
    vote_num = scrapy.Field()  # 电影评分人数
    rating_per_stars5 = scrapy.Field()  # 电影5分百分比
    rating_per_stars4 = scrapy.Field()  # 电影4分百分比
    rating_per_stars3 = scrapy.Field()  # 电影3分百分比
    rating_per_stars2 = scrapy.Field()  # 电影2分百分比
    rating_per_stars1 = scrapy.Field()  # 电影1分百分比
    intro = scrapy.Field()  # 电影剧情简介
    comment_num = scrapy.Field()  # 电影短评数
    question_num = scrapy.Field()  # 电影提问数

class DoubanMovieBriefItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_id = scrapy.Field()  # 电影的唯一ID