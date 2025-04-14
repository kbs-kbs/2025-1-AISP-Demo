import subprocess

def crawl():
    # 별도 프로세스로 Scrapy 실행
    subprocess.run([
        "scrapy", "crawl", "rankings"
    ])

if __name__ == '__main__':
    # 크롤러 실행 및 CSV 병합
    crawl()