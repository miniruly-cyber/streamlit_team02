설치 & 실행

1) 가상환경 + 패키지 설치
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
# .venv\Scripts\activate

pip install -U pip
pip install -r requirements.txt

2) 환경변수(선택)
# LLM 개선안 사용 시
export OPENAI_API_KEY=sk-...

# (선택) 웹 리서치 사용 시
export SERPAPI_API_KEY=...
export BING_API_KEY=...

# (선택) CSV 경로 지정 (기본은 /mnt/data 우선)
export DATA_DIR=./data

3)  데이터 배치
	•	/mnt/data 또는 프로젝트 루트(./) 중 존재하는 경로에 CSV 배치
	•	최소 권장: job_market.csv, skills_analysis.csv

4) 실행
streamlit run test.py
