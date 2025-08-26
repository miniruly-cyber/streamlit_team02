# Requirements (install first):
#   pip install streamlit python-docx reportlab langchain langchain-openai python-dotenv

import os, io, json, time, textwrap, re, datetime, urllib.parse
import streamlit as st
from typing import Optional, Tuple

# ===== LangChain imports (조건부) =====
try:
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.memory import ConversationBufferMemory
    from langchain.chains import LLMChain
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    st.warning("LangChain이 설치되지 않았습니다. pip install langchain langchain-openai 명령으로 설치해주세요.")

# ================= 기본 설정 =================
st.set_page_config(page_title="자기소개서 코치 (LangChain)", page_icon="💬", layout="wide")

# 모바일 친화적 스타일 적용
st.markdown("""
<style>
.main .block-container {
    max-width: 800px;
    padding-top: 1rem;
    padding-bottom: 1rem;
}

.round-header {
    margin: 12px 0 8px;
    background: linear-gradient(135deg, #0FBDBD, #099494);
    color: #fff;
    border-radius: 18px;
    padding: 14px 18px;
    box-shadow: 0 8px 20px rgba(0,0,0,.08);
}

.round-header__title {
    font-weight: 900;
    letter-spacing: .2px;
    margin: 0;
    font-size: 1.2em;
}

.round-header__sub {
    opacity: .95;
    font-size: 0.9em;
    margin-top: 4px;
}

.bubble {
    margin: 10px 0;
    display: flex;
}

.bubble.bot {
    justify-content: flex-start;
}

.bubble.me {
    justify-content: flex-end;
}

.bubble-content {
    max-width: 70%;
}

.bubble-text {
    padding: 10px 14px;
    border-radius: 18px;
    word-wrap: break-word;
    line-height: 1.5;
}

.bubble.bot .bubble-text {
    background: #F3F4F6;
    border-radius: 18px 18px 18px 4px;
}

.bubble.me .bubble-text {
    background: #E8FDFC;
    border-radius: 18px 18px 4px 18px;
}

.bubble-time {
    font-size: 11px;
    color: #64748b;
    margin-top: 4px;
    padding: 0 14px;
}

.chat-container {
    height: 400px;
    overflow-y: auto;
    padding: 10px;
    background: white;
    border-radius: 10px;
    margin-bottom: 20px;
}

/* 탭 스타일 개선 */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    padding-left: 20px;
    padding-right: 20px;
    background-color: white;
    border-radius: 10px;
}

.stTabs [aria-selected="true"] {
    background-color: #0FBDBD;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ================= 상태 초기화 =================
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.msgs = []
    st.session_state.settings = {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "tone": "정중하고 간결한",
        "length": 800,
        "temperature": 0.7,
        "openai_key": os.getenv("OPENAI_API_KEY", ""),
        "gemini_key": os.getenv("GEMINI_API_KEY", ""),
        "save_dir": os.path.expanduser("~/AI_CoverLetter_Storage")
    }
    # 초기 메시지 추가
    st.session_state.msgs.append({
        "role": "bot",
        "content": "안녕하세요! 자기소개서 작성을 도와드릴게요. 어떤 회사/직무에 지원하시나요?",
        "timestamp": datetime.datetime.now().strftime("%p %I:%M")
    })

# ===== LangChain 메모리 설정 =====
if LANGCHAIN_AVAILABLE and "lc_memory" not in st.session_state:
    st.session_state.lc_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ================= 유틸리티 함수 =================
def now_hhmm():
    return datetime.datetime.now().strftime("%p %I:%M").replace("AM", "오전").replace("PM", "오후")

def timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def slugify(name: str) -> str:
    return (re.sub(r'[\\/:*?"<>|]', "_", name).strip() or "coverletter")

def header_card(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div class="round-header">
      <div class="round-header__title">{title}</div>
      {f'<div class="round-header__sub">{subtitle}</div>' if subtitle else ''}
    </div>""", unsafe_allow_html=True)

# ================= AI 챗봇 로직 =================
def get_ai_response(user_message: str) -> str:
    """LangChain을 사용한 AI 응답 생성"""
    if not LANGCHAIN_AVAILABLE:
        return "LangChain이 설치되지 않았습니다. 데모 모드로 실행중입니다.\n\n자기소개서 작성 팁: 구체적인 경험과 성과를 수치와 함께 제시하세요."
    
    try:
        settings = st.session_state.settings
        
        # OpenAI API 키가 있는 경우에만 실제 API 호출
        if settings["openai_key"]:
            llm = ChatOpenAI(
                api_key=settings["openai_key"],
                model=settings["model"],
                temperature=settings["temperature"]
            )
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", f"""
                당신은 자기소개서 작성을 도와주는 전문 코치입니다.
                - 톤: {settings["tone"]}
                - 목표 길이: 약 {settings["length"]}자
                - 구체적이고 실용적인 조언을 제공하세요
                - 사용자의 경험을 바탕으로 개선점을 제안하세요
                """),
                ("human", "{input}")
            ])
            
            chain = LLMChain(llm=llm, prompt=prompt, memory=st.session_state.lc_memory)
            response = chain.run(input=user_message)
            return response
        else:
            # 데모 응답 (API 키가 없을 때)
            demo_responses = {
                "마케팅": "마케팅 직무 자기소개서에서는 데이터 분석 능력, 창의성, 커뮤니케이션 스킬을 강조하세요. 특히 캠페인 성과를 구체적인 수치로 제시하면 좋습니다.",
                "개발": "개발 직무에서는 사용 가능한 기술 스택, 프로젝트 경험, 문제 해결 사례를 구체적으로 작성하세요.",
                "영업": "영업 직무는 목표 달성률, 고객 관계 관리, 협상 능력을 중심으로 작성하세요.",
                "default": "자기소개서 작성 시 STAR 기법(Situation-Task-Action-Result)을 활용하여 구체적인 경험을 서술하세요."
            }
            
            for keyword, response in demo_responses.items():
                if keyword in user_message:
                    return f"[데모 모드]\n\n{response}\n\n실제 AI 기능을 사용하려면 설정 탭에서 OpenAI API 키를 입력해주세요."
            
            return f"[데모 모드]\n\n{demo_responses['default']}\n\n실제 AI 기능을 사용하려면 설정 탭에서 OpenAI API 키를 입력해주세요."
            
    except Exception as e:
        return f"죄송합니다. 오류가 발생했습니다: {str(e)}"

# ================= 메인 UI 함수들 =================
def render_chat_tab():
    """채팅 탭 렌더링"""
    header_card("💬 AI 자기소개서 코치", "개인맞춤형 자기소개서 작성 도우미")
    
    # 채팅 메시지 표시 영역
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.msgs:
            bubble_class = "bot" if msg["role"] == "bot" else "me"
            
            html_content = f"""
            <div class="bubble {bubble_class}">
                <div class="bubble-content">
                    <div class="bubble-text">{msg["content"]}</div>
                    <div class="bubble-time">{msg.get("timestamp", now_hhmm())}</div>
                </div>
            </div>
            """
            st.markdown(html_content, unsafe_allow_html=True)
    
    # 입력 영역
    st.markdown("---")
    
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input(
                "메시지를 입력하세요...", 
                placeholder="예: 마케팅 직무 자기소개서 작성법을 알려주세요",
                label_visibility="collapsed"
            )
        with col2:
            submit = st.form_submit_button("전송", use_container_width=True, type="primary")
        
        if submit and user_input:
            # 사용자 메시지 추가
            st.session_state.msgs.append({
                "role": "user",
                "content": user_input,
                "timestamp": now_hhmm()
            })
            
            # AI 응답 생성
            with st.spinner("AI가 답변을 생성중입니다..."):
                ai_response = get_ai_response(user_input)
                st.session_state.msgs.append({
                    "role": "bot",
                    "content": ai_response,
                    "timestamp": now_hhmm()
                })
            
            st.rerun()

def render_settings_tab():
    """설정 탭 렌더링"""
    header_card("⚙️ 설정", "AI 모델 및 응답 설정")
    
    settings = st.session_state.settings
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔑 API 키 설정")
        new_key = st.text_input(
            "OpenAI API Key", 
            value=settings["openai_key"], 
            type="password", 
            help="gpt-4o-mini 모델 사용을 위한 API 키"
        )
        
        st.subheader("🤖 모델 설정")
        new_model = st.selectbox(
            "모델 선택", 
            ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], 
            index=["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"].index(settings["model"])
        )
        new_temp = st.slider("창의성 수준", 0.0, 1.0, settings["temperature"], 0.1)
    
    with col2:
        st.subheader("📝 응답 설정")
        new_tone = st.selectbox(
            "응답 톤", 
            ["정중하고 간결한", "친근하고 상세한", "전문적이고 격식있는"],
            index=["정중하고 간결한", "친근하고 상세한", "전문적이고 격식있는"].index(settings["tone"])
        )
        new_length = st.slider("목표 응답 길이 (자)", 200, 2000, settings["length"], 100)
    
    if st.button("설정 저장", use_container_width=True, type="primary"):
        st.session_state.settings["openai_key"] = new_key
        st.session_state.settings["model"] = new_model
        st.session_state.settings["temperature"] = new_temp
        st.session_state.settings["tone"] = new_tone
        st.session_state.settings["length"] = new_length
        st.success("✅ 설정이 저장되었습니다!")

def render_storage_tab():
    """저장소 탭 렌더링"""
    header_card("💾 대화 기록", "작성한 자기소개서 관리")
    
    if len(st.session_state.msgs) > 1:
        st.subheader("📋 현재 대화 내용")
        
        # 대화 내용을 텍스트로 변환
        conversation_text = ""
        for msg in st.session_state.msgs:
            if msg["role"] == "user":
                conversation_text += f"👤 사용자: {msg['content']}\n\n"
            else:
                conversation_text += f"🤖 AI 코치: {msg['content']}\n\n"
            conversation_text += "---\n\n"
        
        # 다운로드 버튼
        st.download_button(
            label="💾 대화 내용 다운로드 (TXT)",
            data=conversation_text,
            file_name=f"자기소개서_상담_{timestamp()}.txt",
            mime="text/plain"
        )
        
        # 대화 내용 표시
        with st.expander("대화 내용 미리보기", expanded=True):
            st.text_area("", value=conversation_text, height=400, disabled=True)
        
        # 대화 초기화 버튼
        if st.button("🗑️ 대화 내용 초기화", type="secondary"):
            st.session_state.msgs = [{
                "role": "bot",
                "content": "안녕하세요! 자기소개서 작성을 도와드릴게요. 어떤 회사/직무에 지원하시나요?",
                "timestamp": now_hhmm()
            }]
            if LANGCHAIN_AVAILABLE:
                st.session_state.lc_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
            st.success("대화 내용이 초기화되었습니다.")
            st.rerun()
    else:
        st.info("아직 저장된 대화 내용이 없습니다. 채팅 탭에서 대화를 시작해보세요!")

# ================= 메인 앱 로직 =================
def main():
    """메인 앱 실행"""
    
    # 앱 제목
    st.title("📱 AI 자기소개서 코치")
    st.caption("LangChain 기반 맞춤형 자기소개서 작성 도우미")
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["💬 채팅", "⚙️ 설정", "💾 대화 기록"])
    
    with tab1:
        render_chat_tab()
    
    with tab2:
        render_settings_tab()
    
    with tab3:
        render_storage_tab()
    
    # 하단 정보
    st.markdown("---")
    st.caption("💡 Tip: OpenAI API 키가 없어도 데모 모드로 기본 기능을 체험할 수 있습니다.")

# ================= 앱 실행 =================
if __name__ == "__main__":
    main()
