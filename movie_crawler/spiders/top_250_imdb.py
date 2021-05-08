import scrapy

from movie_crawler.items import MovieItem
from movie_crawler.common import config



class ImdbSpider(scrapy.Spider):
    xpaths = config()['movie_sites']['imdb']['xpaths']
    
    name = 'top_250_imdb'
    start_urls = ['http://www.imdb.com/chart/top/']
    
    def parse(self, response):
        """
        Scrapy creates scrapy.http.Request objects for each URL in the start_ursl
        attribute of the Spider, and assigns them the parse method of the spider
        sa their callback function
        """
        # Links to the movie pages
        movies =  response.xpath('//tbody[@class="lister-list"]//td[@class="titleColumn"]/a/@href').getall()[:1]
        for movie in movies:
            yield response.follow(movie, callback=self.parse_movie)            

    
    def parse_movie(self, response):
        item = MovieItem()
        item['url'] = response.url

        # Requests that return only one value
        returns_unique = ['title','rating','duration','release_date','rating_count','filming_locations',
                          'director','storyline','certificate','aka','country','language','aspect_ratio',
                          'budget','gross_usa','opening_weekend_usa','color','sound_mix',
                          'cumulative_gross','poster']

        # Requests that return a list
        returns_list   = ['writers','stars','genres','keywords','cast', 'summary']

        for key in returns_unique:
            item[key] = response.xpath(self.xpaths[key]).get()

        for key in returns_list:
            item[key] = response.xpath(self.xpaths[key]).getall()

        
        link_to_reviews = response.xpath(self.xpaths['link_to_reviews']).get()
        yield response.follow(link_to_reviews, callback=self.parse_reviews, cb_kwargs=dict(item=item))

    
    def parse_reviews(self, response, item):
        item['reviews'] = []

        reviews = response.xpath(self.xpaths['reviews'])
        for review in reviews:
            item['reviews'].append(' '.join(review.xpath('text()').getall()))

        yield item 


        