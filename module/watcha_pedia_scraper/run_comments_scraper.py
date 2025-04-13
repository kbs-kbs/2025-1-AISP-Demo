from scrapy.crawler import CrawlerProcess
from scrpy_plwrt_demo.spiders.comments import CommentsSpider

def run_comments_scraper():
    process = CrawlerProcess(settings={
        "FEEDS": {
            "output.css": {"format": "css"},
        },
    })
    process.crawl(CommentsSpider)
    process.start()