import scrapy
from scrpy_plwrt_demo.items import ThumbnailItem
import time

class RankingsSpider(scrapy.Spider):
    name = 'rankings'
    allowed_domains = ['pedia.watcha.com']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = time.time()

    def start_requests(self):
        url = "https://pedia.watcha.com/ko-KR/?domain=movie"
        yield scrapy.Request(url, self.parse)
        
    def parse(self, response):
        for section in ['box_office', 'watcha', 'netflix']:
            yield from self.process_section(response, section)
        
    def process_section(self, response, section):
        if section == 'watcha':
            self.inform('섹션', section)
        section_nums = {
            'box_office': 1,
            'watcha': 5,
            'netflix': 7,
        }
        items = response.css(f'#root > div:nth-of-type(1) > section > div > section > div:nth-of-type({section_nums[section]}) > section > div.listWrapper > ul > li')
        for i, item in enumerate(items):
            thumbnail = ThumbnailItem()
            thumbnail['section'] = section
            thumbnail['ranking'] = i + 1
            thumbnail['title'] = item.css('a > div:nth-of-type(2) > div:nth-of-type(1)::text').get()
            thumbnail['release_year'] = item.css('a > div:nth-of-type(2) > div:nth-of-type(2)::text').get().split()[0]
            thumbnail['country'] = item.css('a > div:nth-of-type(2) > div:nth-of-type(2)::text').get().split()[-1]
            description = item.css('a > div:nth-of-type(2) > div:nth-of-type(4)::text').get()
            if description:
                thumbnail['reservation'] = description.split()[1]
                thumbnail['audience'] = description.split()[-1]
            else:
                thumbnail['reservation'] = ''
                thumbnail['audience'] = ''
            thumbnail['image_url'] = item.css('a > div:nth-of-type(1) > div:nth-of-type(1) > img[src]').get()
            
            yield thumbnail

    # 디버깅을 위한 로그 출력 함수
    def inform(self, name, value, *args):
        info = { name: value }
        if args:
            info.update({ args[i]: args[i + 1] for i in range(0, len(args), 2) })
        self.logger.info(f'{info} ({(time.time() - self.start_time):.1f}초)')
