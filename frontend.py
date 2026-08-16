import streamlit as st
from langchain_core.messages import HumanMessage
from backend import execute
import uuid

st.title("🌐 Chat Sphere")
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())
message_history = []
config = {"configurable":{"thread_id":st.session_state["thread_id"]}}
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
   
    
    with st.chat_message("ai",avatar="🤖"):
        ai_stream_response = execute.stream(user_message,config=config,stream_mode="messages")
        ai_response = st.write_stream(message_chunk.content for message_chunk,metadata in ai_stream_response)
    st.session_state["message_history"].append({"role":"ai","content":ai_response, "avatar":"🤖"})
        