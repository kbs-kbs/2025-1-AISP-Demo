import scrapy

class ThumbnailItem(scrapy.Item):
    ranking=scrapy.Field()
    title=scrapy.Field()
    release_year=scrapy.Field()
    country=scrapy.Field()
    reservation=scrapy.Field()
    audience=scrapy.Field()

