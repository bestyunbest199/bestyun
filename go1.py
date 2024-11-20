import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

# 페이지 기본 설정
st.set_page_config(
    page_title="심리상담 AI 챗봇",
    page_icon="🤗",
    layout="wide"
)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

def initialize_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# 사이드바에 API 키 입력
with st.sidebar:
    st.title("설정")
    api_key = st.text_input("Gemini API 키를 입력하세요", type="password")
    uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")
    
    if uploaded_file:
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.success("PDF 파일이 성공적으로 업로드되었습니다!")

# 메인 페이지
st.title("🤗 AI 심리상담 챗봇")
st.write("당신의 이야기를 들려주세요. AI 상담사가 도와드리겠습니다.")

# API 키가 입력된 경우에만 챗봇 활성화
if api_key:
    model = initialize_gemini(api_key)
    
    # 시스템 프롬프트 설정
    system_prompt = """
    당신은 전문 심리상담사입니다. 사용자의 고민을 경청하고 공감하며, 
    전문적인 조언을 제공해주세요. 항상 따뜻하고 지지적인 태도를 유지하며,
    필요한 경우 전문가 상담을 권유해주세요.
    """
    
    # 채팅 인터페이스
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("메시지를 입력하세요"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            context = system_prompt
            if uploaded_file:
                context += f"\n참고할 문서 내용: {pdf_text}"
            
            response = model.generate_content(context + "\n사용자: " + prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

else:
    st.warning("Gemini API 키를 입력해주세요.")

# 푸터
st.markdown("---")
st.markdown("⚠️ 이 AI 상담 서비스는 전문 상담사를 대체할 수 없으며, 심각한 심리적 어려움이 있는 경우 반드시 전문가와 상담하시기 바랍니다.")
