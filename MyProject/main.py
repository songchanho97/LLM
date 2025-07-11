import streamlit as st
from langchain_core.messages.chat import ChatMessage

st.title("나만의 챗GPT")

# 처음 1번만 실행
if "messages" not in st.session_state:
    # 대화기록을 저장하기 위한 용도
    st.session_state["messages"] = []

def print_messages():
    """대화기록을 출력하는 함수"""
    for message in st.session_state["messages"]:
        st.chat_message(message.role).write(message.content)

def add_message(role, message):
    """대화기록을 추가하는 함수"""
    st.session_state["messages"].append(ChatMessage(role=role, content=message))

print_messages()

# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요")
if user_input:
    # 웹에 대화를 출력
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(user_input)

    # 대화기록을 저장    
    add_message("user", user_input)
    add_message("assistant", user_input)
