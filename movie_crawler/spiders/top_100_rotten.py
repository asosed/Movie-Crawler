import scrapy

from movie_crawler.items import MovieItem
from movie_crawler.common import config


class RottenSpider(scrapy.Spider):
    xpaths = config()['movie_sites']['rotten']['xpaths']

    name = 'top_100_rotten'
    start_urls = ['https://www.rottentomatoes.com/top/bestofrt/']

    def parse(self, response):
        """
        Scrapy creates scrapy.http.Request objects for each URL in the start_ursl
        attribute of the Spider, and assigns them the parse method of the spider
        sa their callback function
        """
        # Links to the movie pages
        movies = response.xpath('//table[@class="table"]//@href')[:3]
        for movie in movies:
            yield response.follow(movie, callback=self.parse_movie)


    def parse_movie(self, response):
        item = MovieItem()
        item['url'] = response.url

        # Requests that return only one value
        returns_unique = ['title','rating','duration','release_date','rating_count',
                          'director','summary','gross_usa','sound_mix','aspect_ratio',
                          'poster','genres']

        # Requests that return a list
        returns_list   = ['writers','cast']

        for key in returns_unique:
            item[key] = response.xpath(self.xpaths[key]).get()

        for key in returns_list:
            item[key] = response.xpath(self.xpaths[key]).getall()

        yield item