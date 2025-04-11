# 최초 환경 설정
1. `winget install --id=Python.Python.3.13 -e`
2. `configurator.bat`
3. `python3.13 -m venv venv`
4. `venv\Scripts\activate` 및 편집기에서 가상환경 활성화
5. `pip3.13 install -r requirements.txt`
6. `playwright install`

# 환경 설정 및 실행
1. `venv\Scripts\activate` 및 편집기에서 가상환경 활성화
2. `python pipeline.py`: 실행

# 도메인별로 따로 실행
1. `venv\Scripts\activate` 및 편집기에서 가상환경 활성화
2. `scrapy crawl ranking -O csv/ranking.csv`: dbpia 크롤링 + csv로 저장
3. `scrapy crawl comments -O csv/comments.csv -a movie_id=mdKpkjk`: riss 크롤링 + csv로 저장
