import scrapy

class ThesisItem(scrapy.Item):
    ranking=scrapy.Field()
    title=scrapy.Field()
    release_year=scrapy.Field()
    country=scrapy.Field()
    reservation=scrapy.Field()
    audience=scrapy.Field()

class CommentItem(scrapy.Item):
    user=scrapy.Field()
    comment=scrapy.Field()
    like=scrapy.Field()

class ThumbnailItem(scrapy.Item):
    ranking=scrapy.Field()
    title=scrapy.Field()
    release_year=scrapy.Field()
    country=scrapy.Field()
    reservation=scrapy.Field()
    audience=scrapy.Field()

