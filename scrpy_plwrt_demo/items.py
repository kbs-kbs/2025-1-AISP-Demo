import scrapy

class CommentItem(scrapy.Item):
    user=scrapy.Field()
    comment=scrapy.Field()
    like=scrapy.Field()

class ThumbnailItem(scrapy.Item):
    section=scrapy.Field()
    rank=scrapy.Field()
    title=scrapy.Field()
    release_year=scrapy.Field()
    country=scrapy.Field()
    reservation=scrapy.Field()
    audience=scrapy.Field()
    image_url=scrapy.Field()
    url=scrapy.Field()

class MovieItem(scrapy.Item):
    title=scrapy.Field()
    en_title=scrapy.Field()
    release_year=scrapy.Field()
    country=scrapy.Field()
    genre=scrapy.Field()
    running_time=scrapy.Field()
    rating=scrapy.Field()
    description=scrapy.Field()
    cast=scrapy.Field()
    image_url=scrapy.Field()

