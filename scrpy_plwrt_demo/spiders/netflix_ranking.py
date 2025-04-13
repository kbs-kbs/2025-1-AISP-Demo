import scrapy
from scrpy_plwrt_demo.items import ThumbnailItem
import time

class NetflixRankingSpider(scrapy.Spider):
    name = 'netflix_ranking'
    allowed_domains = ['pedia.watcha.com']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = time.time()

    def start_requests(self):
        url = "https://pedia.watcha.com/ko-KR/?domain=movie"
        yield scrapy.Request(url, self.parse)
        
    def parse(self, response):
        items = response.css('#root > div.nth-of-type(1) > section > div > section > div:nth-of-type(7) > section > div.listWrapper > ul > li')
        for i, item in enumerate(items):
            thumbnail = ThumbnailItem()
            thumbnail['ranking'] = i + 1
            thumbnail['title'] = item.css('a > div:nth-of-type(2) > div:nth-of-type(1)::text').get()
            thumbnail['release_year'] = item.css('a > div:nth-of-type(2) > div:nth-of-type(2)::text').get().split()[0]
            thumbnail['country'] = item.css('a > div:nth-of-type(2) > div:nth-of-type(2)::text').get().split()[-1]
            thumbnail['reservation'] = ''
            thumbnail['audience'] = ''
            
            yield thumbnail

    # 디버깅을 위한 로그 출력 함수
    def inform(self, name, value, *args):
        info = { name: value }
        if args:
            info.update({ args[i]: args[i + 1] for i in range(0, len(args), 2) })
        self.logger.info(f'{info} ({(time.time() - self.start_time):.1f}초)')
