# 최초 환경 설정
## 1. Powershell로 uv 설치
1. `Set-ExecutionPolicy RemoteSigned Process`
2. `irm https://astral.sh/uv/install.ps1 | iex`

## 2. Command Prompt로 의존성 패키지 설치
1. `uv sync`
2. `uv run playwright install`

# 실행
1. `uv run streamlit run app.py`

# 모듈별 실행
```bash
uv run module\watcha_pedia_crawler\rankings_crawler.py
```
```bash
uv run module\watcha_pedia_crawler\comments_crawler.py
```