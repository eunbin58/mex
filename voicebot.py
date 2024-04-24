import streamlit as st
from datetime import datetime
import openai


def ask_gpt(prompt, model, apikey):
    client = openai.OpenAI(api_key = apikey)
    response = client.chat.completions.create(
        model=model,
        messages=prompt)
    gptResponse = response.choices[0].message.content
    return gptResponse

def main():
    st.set_page_config(
        page_title="채팅 프로그램",
        layout="wide"
    )
    st.header("채팅 프로그램")

    st.markdown("---")

    with st.expander("채팅 프로그램에 관하여", expanded=True):
        st.write(
            """
            202004052 박은빈 중간고사
            
            """
        )

        st.markdown("")

    if "chat" not in st.session_state:
        st.session_state["chat"]=[]

    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENAI_API"]=""

    if "messages" not in st.session_state:
        st.session_state["messages"]=[{"role":"system","content":"You are a thoughtful assistant."}]

    if "check_audio" not in st.session_state:
        st.session_state["check_reset"]=False
    
    with st.sidebar:

        st.session_state["OPENAI_API"]=st.text_input(label="OPENAI API 키", placeholder="Enter Your API Key", value="", type="password")

        st.markdown("---")

        model =st.radio(label="GPT 모델", options=["gpt-4","gpt-3.5-turbo"])

        st.markdown("---")

        if st.button(label="초기화"):
            st.session_state["chat"]=[]
            st.session_state["messages"]=[{"role":"system","content":"You are a thoughtful assistant. Respond to all input in 25 words and answer in korea"}]
            st.session_state["check_rest"]=True

    col1, col2=st.columns(2)
    with col1:
        st.subheader("질문하기")
        user_input=st.text_input(label="",placeholder="텍스트로 질문", value="",key="user_input")
        bt=st.button("제출")
        if bt:
            if user_input and not(st.session_state["check_reset"]):
                now=datetime.now().strftime("%H:%M")
                st.session_state["chat"]=st.session_state["chat"]+[("user",now,user_input)]
                st.session_state["messages"]=st.session_state["messages"]+[{"role":"user","content":user_input}]
            

    with col2:
        st.subheader("질문/답변")
        if(user_input)and (st.session_state["check_reset"]==False):
            response = ask_gpt(st.session_state["messages"], model, st.session_state["OPENAI_API"])

            st.session_state["messages"]=st.session_state["messages"]+[{"role":"assistant","content":response}]

            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"]=st.session_state["chat"]+[("bot",now, response)]
            
            for sender, time, message in st.session_state["chat"]:
                if sender == "user":
                    st.write(f'<div style="display:flex;align-items:center;"><div style="background-color:#007AFF;color:white;border-radius:12px;padding:8px 12px;margin-right:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                    st.write("")
                else:
                    st.write(f'<div style="display:flex;align-items:center;justify-content:flex-end;"><div style="background-color:lightgray;border-radius:12px;padding:8px 12px;margin-left:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                    st.write("")



if __name__=="__main__":
    main()

