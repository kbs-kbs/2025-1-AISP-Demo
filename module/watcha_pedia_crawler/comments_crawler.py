import subprocess

def crawl(movie_id):
    # 별도 프로세스로 Scrapy 실행
    subprocess.run([
        "scrapy", "crawl", "comments", "-O", "csv/comments.csv", "-a", f"movie_id={movie_id}"
    ])

if __name__ == '__main__':
    # 크롤러 실행 및 CSV 병합
    crawl("mdKpkjk") # 야당