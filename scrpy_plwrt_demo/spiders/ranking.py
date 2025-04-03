import scrapy
from scrpy_plwrt_demo.items import ThumbnailItem

class RankingSpider(scrapy.Spider):
    name = 'ranking'
    allowed_domains = ['pedia.watcha.com']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ranking_list = []

    def start_requests(self):
        url = "https://pedia.watcha.com/ko-KR/?domain=movie"
        yield scrapy.Request(url, self.parse_start)
        
    def parse_start(self, response):
        items = response.css('#root > div.kVmNFwyR > section > div > section > div:nth-child(2) > section > div.dmYmGzMK.listWrapper > ul')
        for ranking, item in enumerate(items):
            thumbnail = ThumbnailItem()
            thumbnail['ranking'] = ranking
            thumbnail['title'] = ranking
            thumbnail['release_year'] = ranking
            thumbnail['ranking'] = ranking
            