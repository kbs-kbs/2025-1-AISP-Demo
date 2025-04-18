import scrapy
from scrapy_playwright.page import PageMethod
from scrpy_plwrt_demo.items import ThumbnailItem
import time

class RankingsSpider(scrapy.Spider):
    name = 'rankings'
    allowed_domains = ['pedia.watcha.com']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = time.time()

    def start_requests(self):
        yield scrapy.Request(
            url="https://pedia.watcha.com/ko-KR/?domain=movie",
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("evaluate", "document.body.style.zoom = 0.25"),
                    PageMethod("wait_for_selector", "#root > div:nth-of-type(1) > section > div > section > div:nth-of-type(7) > section > div.listWrapper > ul > li")
                ],
            },
            callback=self.parse)
        
    def parse(self, response):
        for section in ['box_office', 'watcha', 'netflix']:
            yield from self.process_section(response, section)
        
    def process_section(self, response, section):
        self.inform('섹션', section)
        section_nums = {
            'box_office': 1,
            'watcha': 5,
            'netflix': 7
        }
        items = response.css(f'#root > div:nth-of-type(1) > section > div > section > div:nth-of-type({section_nums[section]}) > section > div.listWrapper > ul > li')
        for i, item in enumerate(items):
            thumbnail = ThumbnailItem()
            thumbnail['section'] = section
            thumbnail['rank'] = i + 1
            thumbnail['title'] = item.css('a > div:nth-of-type(2) > div:nth-of-type(1)::text').get()
            thumbnail['release_year'] = item.css('a > div:nth-of-type(2) > div:nth-of-type(2)::text').get().split()[0]
            thumbnail['country'] = item.css('a > div:nth-of-type(2) > div:nth-of-type(2)::text').get().split()[-1]
            thumbnail_details = item.css('a > div:nth-of-type(2) > div:nth-last-of-type(1)::text').get()
            if thumbnail_details:
                thumbnail['reservation'] = thumbnail_details.split()[1]
                thumbnail['audience'] = thumbnail_details.split()[-1]
            else:
                thumbnail['reservation'] = '집계 중'
                thumbnail['audience'] = '집계 중'
            thumbnail['movie_id'] = item.css('a::attr(href)').get().split('/')[-1]
            thumbnail['image_url'] = item.css('a > div:nth-of-type(1) > div:nth-of-type(1) > img::attr(src)').get()

            yield thumbnail

    def inform(self, name, value, *args):
        info = { name: value }
        if args:
            info.update({ args[i]: args[i + 1] for i in range(0, len(args), 2) })
        self.logger.info(f'{info} ({(time.time() - self.start_time):.1f}초)')
