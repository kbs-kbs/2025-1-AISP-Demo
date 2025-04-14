import scrapy

class CommentItem(scrapy.Item):
    user=scrapy.Field()
    comment=scrapy.Field()
    like=scrapy.Field()

class ThumbnailItem(scrapy.Item):
    section=scrapy.Field()
    ranking=scrapy.Field()
    title=scrapy.Field()
    release_year=scrapy.Field()
    country=scrapy.Field()
    reservation=scrapy.Field()
    audience=scrapy.Field()
    image_url=scrapy.Field()

