# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    aka = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    duration = scrapy.Field()
    keywords = scrapy.Field()
    storyline = scrapy.Field()
    certificate = scrapy.Field()
    year_release = scrapy.Field()
    release_date = scrapy.Field()
    genres = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    filming_locations = scrapy.Field()
    budget = scrapy.Field()
    opening_weekend_usa = scrapy.Field()
    gross_usa = scrapy.Field()
    cumulative_gross = scrapy.Field()
    sound_mix = scrapy.Field()
    color = scrapy.Field()
    aspect_ratio = scrapy.Field()
    rating = scrapy.Field()
    rating_count = scrapy.Field()
    director = scrapy.Field()
    writers = scrapy.Field()  
    stars =  scrapy.Field()
    summary = scrapy.Field()
    cast = scrapy.Field()
    poster = scrapy.Field()
