import streamlit as st
from langchain_core.messages.chat import ChatMessage
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_teddynote.prompts import load_prompt
from langsmith import Client

load_dotenv(dotenv_path='.env')

import os
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

st.title("나만의 챗GPT🐎")

# 처음 1번만 실행
if "messages" not in st.session_state:
    # 대화기록을 저장하기 위한 용도
    st.session_state["messages"] = []

# 사이드바 생성
with st.sidebar:
    clear_btn = st.button("초기화")

    selected_prompt = st.selectbox(
    "프롬프트를 선택해주세요", ("기본모드", "SNS 게시글", "요약"), index=0
)


# 이전 대화를 출력
def print_messages():
    """대화기록을 출력하는 함수"""
    for message in st.session_state["messages"]:
        st.chat_message(message.role).write(message.content)

# 새로운 메시지를 추가
def add_message(role, message):
    """대화기록을 추가하는 함수"""
    st.session_state["messages"].append(ChatMessage(role=role, content=message))

# 체인 생성
def create_chain(prompt_type):
    # prompt | llm | output_parser
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 친절한 AI 어시스턴트입니다."),
        ("user", "#Question:\n{question}"),
    ])
    if prompt_type == "SNS 게시글":
        prompt = load_prompt("prompts/sns.yaml", encoding="utf-8")
    elif prompt_type == "요약":
        # Create a LANGSMITH_API_KEY in Settings > API Keys
        client = Client(api_key=LANGSMITH_API_KEY)
        prompt = client.pull_prompt("teddynote/chain-of-density-korean", include_model=True)

    # GPT
    llm=ChatOpenAI(model_name="gpt-4o", temperature=0.0)
    # 출력 파서
    output_parser = StrOutputParser()

    # 체인 생성
    chain = prompt | llm | output_parser
    return chain

# 초기화 버튼 눌렀을 때
if clear_btn:
    st.session_state["messages"] = []

print_messages()

# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요")


if user_input:
    # 웹에 대화를 출력
    st.chat_message("user").write(user_input)

    # 체인 생성 
    chain = create_chain(selected_prompt)

    # 스트리밍 호출 
    response = chain.stream({"question": user_input})
    with st.chat_message("assistant"):
        # 빈 공간(컨테이너)을 만들어서, 여기에 토큰을 스트리밍 출력한다.
        container = st.empty()

        ai_answer= ""
        for toekn in response:
            ai_answer += toekn
            container.markdown(ai_answer)
    
    # 대화기록을 저장    
    add_message("user", user_input)
    add_message("assistant", ai_answer)
