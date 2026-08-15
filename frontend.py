import streamlit as st
from langchain_core.messages import HumanMessage
from backend import execute

st.title("🌐 Chat Sphere")
message_history = []
config = {"configurable":{"thread_id":"thread_1"}}
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []
else:
    for i in st.session_state["message_history"]:
        with st.chat_message(i["role"],avatar=i["avatar"]):
            st.text(i["content"])
            

user_input = st.chat_input("Type here")

if user_input:
    st.session_state["message_history"].append({"role":"user","content":user_input,"avatar":"👤"})
    with st.chat_message("user", avatar="👤"):
        st.text(user_input)
    user_message = {"messages":user_input}
    ai_response = execute.invoke(user_message,config=config)
    st.session_state["message_history"].append({"role":"ai","content":ai_response["messages"][-1].content, "avatar":"🤖"})
    with st.chat_message("ai",avatar="🤖"):
        st.text(ai_response["messages"][-1].content)