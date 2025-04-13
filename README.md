# 최초 환경 설정
## 1. Powershell로 uv 설치
1. `Set-ExecutionPolicy RemoteSigned Process`
2. `irm https://astral.sh/uv/install.ps1 | iex`

## 2. Command Prompt로 의존성 패키지 설치
1. `uv sync`
2. `uv run playwright install`

# 실행
1. `uv run streamlit run app.py`

# 도메인별로 실행
## 박스 오피스 순위 Top 10
```python
uv run scrapy crawl ranking -O csv/ranking.csv
```
## 왓챠 영화 Top 10
```python
uv run scrapy crawl watcha_ranking -O csv/ranking.csv
```
## 영화 최신 코멘트 Top 900
```python
uv run scrapy crawl comments -O csv/comments.csv -a movie_id=m5ekxEM
```
