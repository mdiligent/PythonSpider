import scrapy
import re
from douban.items import DoubanMovieBriefItem

class MovieId250Spider(scrapy.Spider):
    name = 'movie-id-250'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']
    custom_settings = {
        'ITEM_PIPELINES': {
            'douban.pipelines.IDItemPipeline': 1,
        }
    }

    def parse(self, response):
        item = DoubanMovieBriefItem()
        movie_list = response.xpath('//div[@id="content"]//ol/li')
        print("个数:", len(movie_list))
        for movie_item in movie_list:
            href= movie_item.xpath('./div[@class="item"]/div[@class="pic"]/a/@href').extract_first()
            #movieid获取的方法不太好，如果网址中又数字就比较麻烦
            #另外写入movie_id.out的文件应该是纯数字而不是字典
            item['movie_id'] = re.search(r'/(\d+)/', href).group(1)
            print(item)
            yield item
        next_link = response.xpath('//span[@class="next"]/link/@href').extract()
        if next_link:
            # 进行回调
            next_link = next_link[0]
            # https://movie.douban.com/top250
            # next_link= ?start=175&filter=
            yield scrapy.Request('https://movie.douban.com/top250' + next_link, callback=self.parse)
