import scrapy
from scrapy_playwright.page import PageMethod
from playwright.async_api import async_playwright
import time
from scrpy_plwrt_demo.items import CommentItem

class CommentsSpider(scrapy.Spider):
    name = 'comments'
    allowed_domains = ['pedia.watcha.com']
    custom_settings = {
        'FEED_EXPORT_FIELDS': ["user", "comment", "like"],
        'PLAYWRIGHT_ABORT_REQUEST': lambda req: req.resource_type in ['image', 'stylesheet', 'font', 'media']
    }
    
    def __init__(self, movie_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.movie_id = movie_id
        self.start_time = time.time()

    

    def start_requests(self):
        scrolling_script = """
        const scrolls = 20
        let scrollCount = 0

        // scroll down and then wait for 0.5s
        const scrollInterval = setInterval(() => {
          window.scrollTo(0, document.body.scrollHeight)
          scrollCount++

          if (scrollCount === scrolls) {
            clearInterval(scrollInterval)
          }
        }, 500)
        """
        
        yield scrapy.Request(
            url=f'https://pedia.watcha.com/ko-KR/contents/{self.movie_id}/comments',
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "#root > div:nth-of-type(1) > section > section > div > div > div > ul > div"),
                    PageMethod("evaluate", scrolling_script),
                ],
            },
            callback=self.parse
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        scrolls = 20
        scroll_count = 0

        while scroll_count < scrolls:
            # 스크롤 실행
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            # 대기 시간 설정
            await page.wait_for_timeout(500)  # 0.5초

            scroll_count += 1
            print(f"스크롤 횟수: {scroll_count}/{scrolls}")
        
        items = response.css('#root > div:nth-of-type(1) > section > section > div > div > div > ul > div:not(:last-child)')
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
