import subprocess
import pandas as pd

def run_ranking_scraper():
    # 별도 프로세스로 Scrapy 실행
    subprocess.run([
        "scrapy", "crawl", "ranking", "-O", "csv/ranking.csv"
    ])
    
    # 결과 파일 로드
    try:
        df = pd.read_csv("csv/ranking.csv")
        return df
    except Exception as e:
        print(f"파일 읽기 오류: {e}")
        return pd.DataFrame()