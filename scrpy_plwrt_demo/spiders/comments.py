import scrapy
from scrapy.selector import Selector
import time
from scrpy_plwrt_demo.items import CommentItem

class CommentsSpider(scrapy.Spider):
    name = 'comments'
    allowed_domains = ['pedia.watcha.com']
    custom_settings = {
        'FEED_EXPORT_FIELDS': ["user", "comment", "like"]
    }
    
    def __init__(self, movie_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.movie_id = movie_id
        self.start_time = time.time()

    def start_requests(self):
        yield scrapy.Request(
            url=f'https://pedia.watcha.com/ko-KR/contents/{self.movie_id}/comments',
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_goto_kwargs": {
                    "timeout": 200000,
                    "wait_until": "domcontentloaded"
                },
            },
            callback=self.parse
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        page.set_default_timeout(20000)
        await page.wait_for_timeout(5000)
        try:
            last_position = await page.evaluate("window.scrollY")
            while True:
                # scroll by 700 while not at the bottom
                await page.evaluate("window.scrollBy(0, 20000)")
                current_position = await page.evaluate("window.scrollY")
                if current_position == last_position:
                    print("Reached the bottom of the page.")
                    break
                last_position = current_position
                self.inform('스크롤', '스크롤')
        except Exception as error:
            print(f"Error: {error}")
            pass
        
        content = await page.content()
        selector = Selector(text=content)
        items = selector.css('#root > div:nth-of-type(1) > section > section > div > div > div > ul > div:not(:last-child)')
        for item in items:
            comment = CommentItem()
            comment['user'] = item.css('div:nth-of-type(1) > div:nth-of-type(1) > a > div:nth-of-type(2)::text').get()
            comment['comment'] = item.css('div:nth-of-type(2) > a > div > div::text').get()
            comment['like'] = item.css('div:nth-of-type(3) > em:nth-of-type(1)::text').get()
        
            yield comment
        self.inform('스크롤', '끝')
        

    # 디버깅을 위한 로그 출력 함수
    def inform(self, name, value, *args):
        info = { name: value }
        if args:
            info.update({ args[i]: args[i + 1] for i in range(0, len(args), 2) })
        self.logger.info(f'{info} ({(time.time() - self.start_time):.1f}초)')
