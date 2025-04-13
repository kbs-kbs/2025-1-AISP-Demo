# 최초 환경 설정
## 1. Powershell로 UV 설치
1. `Set-ExecutionPolicy RemoteSigned CurrentUser`
2. `irm https://astral.sh/uv/install.ps1 | iex`
3. `Set-ExecutionPolicy Undefined CurrentUser`

## 2. Command Prompt로 의존성 패키지 설치
1. `uv init` 후 `pyproject.toml` 파일 작성
2. `uv python pin 3.12`
3. `uv venv`
4. `uv add -r requirements.txt`
5. `uv sync`
6. `uv run playwright install`

# 실행
1. `uv run python pipeline.py`: 실행

# 도메인별로 실행
## 박스 오피스 순위 Top 10
```python
uv run scrapy crawl ranking -O csv/ranking.csv
```
## 영화 최신 코멘트 Top 900
```python
uv run scrapy crawl comments -O csv/comments.csv -a movie_id=m5ekxEM
```
