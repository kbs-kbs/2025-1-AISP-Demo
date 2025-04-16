import scrapy
from scrapy_playwright.page import PageMethod
import time
from scrpy_plwrt_demo.items import CommentItem


class CommentsSpider(scrapy.Spider):
    name = 'comments'
    allowed_domains = ['pedia.watcha.com']
    custom_settings = {
        'PLAYWRIGHT_ABORT_REQUEST': lambda req: req.resource_type in ['stylesheet', 'image', 'media', 'font'],
        'ITEM_PIPELINES': {},
        'FEED_EXPORT_FIELDS': ["user", "comment", "like"],
    }

    def __init__(self, movie_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.movie_id = movie_id
        self.start_time = time.time()

    def start_requests(self):
        infinite_scroll = """
            () => {
                const enoughCommentCount = 900; // 충분한 댓글 수
                const timeout = 1000; // 1초
                const movieId = window.location.pathname.split('/')[3];
                const originalFetch = window.fetch; // 원본 fetch 백업

                let commentCount = 0;
                let checkTime = Date.now();
                let lastHeight = document.body.scrollHeight;

                window.fetch = async (url, options) => {
                    if (url.includes(`/api/contents/${movieId}/comments`)) {
                        const urlParams = new URL(url).searchParams;
                        const currentPage = parseInt(urlParams.get('page')) || 0;
                        commentCount = currentPage * 9;
                        console.log(`현재 댓글 페이지: ${currentPage} 댓글 수: ${commentCount}`);
                    }
                    return originalFetch(url, options); // 실제 요청 수행
                };
    
                return new Promise(resolve => {
                    const interval = setInterval(() => {
                        if (commentCount > enoughCommentCount) {
                            clearInterval(interval);
                            resolve(true);  // 스크롤 완료
                        }

                        window.scrollTo(0, document.body.scrollHeight);
    
                        if (document.body.scrollHeight === lastHeight) {
                            if (Date.now() - checkTime > timeout) {
                                clearInterval(interval);
                                resolve(true);  // 스크롤 완료
                            }
                        } else {
                            lastHeight = document.body.scrollHeight;
                            checkTime = Date.now();
                        }
                    }, 0);
                });
            }
            """

        yield scrapy.Request(
            url=f"https://pedia.watcha.com/ko-KR/contents/{self.movie_id}/comments?order=recent",
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "#root > div:nth-of-type(1) > section > section > div > div > div > ul > div"),
                    PageMethod("evaluate", "document.body.style.zoom = 0.1"),
                    PageMethod("wait_for_function", infinite_scroll, timeout=200000),
                ],
            },
            callback=self.parse
        )

    def parse(self, response):
        items = response.css(
            '#root > div:nth-of-type(1) > section > section > div > div > div > ul > div:not(:last-child)')
        for item in items:
            comment = CommentItem()
            comment['user'] = item.css(
                'div:nth-of-type(1) > div:nth-of-type(1) > a > div:nth-of-type(2)::text').get()
            comment['comment'] = item.css(
                'div:nth-of-type(2) > a > div > div::text').get()
            comment['like'] = item.css(
                'div:nth-of-type(3) > em:nth-of-type(1)::text').get()

            yield comment

    # 디버깅을 위한 로그 출력 함수

    def inform(self, name, value, *args):
        info = {name: value}
        if args:
            info.update({args[i]: args[i + 1] for i in range(0, len(args), 2)})
        self.logger.info(f'{info} ({(time.time() - self.start_time):.1f}초)')
