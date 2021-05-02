import scrapy

from movie_crawler.items import MovieItem
from movie_crawler.common import config
xpaths = config()['movie_sites']['imdb']['xpaths']


class ImdbSpider(scrapy.Spider):
    name = 'top_250_imdb'
    start_urls = ['http://www.imdb.com/chart/top/']
    
    def parse(self, response):
        """
        Scrapy creates scrapy.http.Request objects for each URL in the start_ursl
        attribute of the Spider, and assigns them the parse method of the spider
        sa their callback function
        """
        # Links to the movie pages
        movies =  response.xpath('//tbody[@class="lister-list"]//td[@class="titleColumn"]/a/@href').getall()
        for movie in movies:
            yield response.follow(movie, callback=self.parse_movie)            

    
    def parse_movie(self, response):
        item = MovieItem()
        item['url'] = response.url

        # Queries that returns only one value
        returns_unique = ['title','rating','year_release','duration','release_date','rating_count',
                          'summary','director','storyline','certificate','aka','country','language',
                          'filming_locations','budget','gross_usa','opening_weekend_usa','color',
                          'sound_mix','aspect_ratio', 'cumulative_gross', 'poster']

        # Queries that returns a list
        returns_list   = ['writers','stars','genres','keywords','cast']

        for key in returns_unique:
            item[key] = response.xpath(xpaths[key]).get()

        for key in returns_list:
            item[key] = response.xpath(xpaths[key]).getall()


        yield item