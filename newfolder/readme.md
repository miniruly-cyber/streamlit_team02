AI 자기소개서 코칭 앱
카카오톡 스타일의 AI 자기소개서 작성 도우미입니다.

🚀 배포된 앱 확인하기
Streamlit Cloud에서 앱 실행하기

✨ 주요 기능
💬 카카오톡 스타일 채팅 인터페이스
🤖 AI 기반 자기소개서 코칭
📄 파일 업로드 및 첨삭
💾 대화 내용 저장
⚙️ 개인화 설정
🛠 설치 및 실행
로컬 환경에서 실행
저장소 클론
bash
git clone https://github.com/your-username/ai-resume-coach.git
cd ai-resume-coach
패키지 설치
bash
pip install -r requirements.txt
환경변수 설정 (선택사항)
bash
# .env 파일 생성
echo "OPENAI_API_KEY=your-api-key-here" > .env
앱 실행
bash
streamlit run app.py
📦 Streamlit Cloud 배포
1단계: GitHub 저장소 생성
GitHub에서 새 저장소 생성
저장소 이름: ai-resume-coach (또는 원하는 이름)
Public으로 설정
2단계: 코드 업로드
bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/ai-resume-coach.git
git push -u origin main
3단계: Streamlit Cloud 배포
Streamlit Cloud에 접속
GitHub 계정으로 로그인
"New app" 클릭
저장소 선택: your-username/ai-resume-coach
Main file path: app.py
"Deploy!" 클릭
4단계: 환경변수 설정 (선택사항)
배포된 앱의 설정 페이지로 이동
"Secrets" 탭 클릭
다음 형식으로 추가:
toml
OPENAI_API_KEY = "your-api-key-here"
📱 사용법
기본 사용
대화 탭: AI와 채팅하며 자기소개서 작성
설정 탭: API 키 설정 및 대화 관리
세부설정 탭: AI 모델 및 저장 설정
저장소 탭: 저장된 대화 파일 관리
효과적인 질문 예시
"마케팅 직무 신입 자기소개서 도입부 작성해줘"
"프로젝트 경험을 STAR 기법으로 정리해줘"
"IT 기업 지원동기 작성 도와줘"
파일 첨삭
.txt 또는 .docx 파일 업로드
"이 내용 첨삭해줘" 메시지와 함께 전송
🔧 기술 스택
Frontend: Streamlit
AI: OpenAI GPT-4 (LangChain)
문서 처리: python-docx, reportlab
배포: Streamlit Cloud
📋 요구사항
Python 3.8+
Streamlit 1.28.0+
OpenAI API Key (선택사항)
🎨 커스터마이징
테마 변경
.streamlit/config.toml 파일에서 색상 변경 가능:

toml
[theme]
primaryColor = "#your-color"
backgroundColor = "#your-bg-color"
AI 응답 개선
get_ai_response() 함수에서 프롬프트 수정 가능

🤝 기여하기
Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request
📝 라이선스
이 프로젝트는 MIT 라이선스를 따릅니다.

🆘 문제 해결
일반적인 문제
Q: 앱이 로딩되지 않아요

A: 브라우저 캐시를 지우고 다시 시도해보세요
Q: AI 응답이 작동하지 않아요

A: OpenAI API 키를 확인하거나, API 키 없이도 기본 기능 사용 가능
Q: 파일 업로드가 안돼요

A: .txt 또는 .docx 파일만 지원합니다
연락처
문제가 지속되면 Issues에 등록해주세요.

Made with ❤️ and Streamlit

