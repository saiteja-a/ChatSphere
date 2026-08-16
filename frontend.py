import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from backend import execute
import uuid

st.title("🌐 Chat Sphere")


# ******************************************
# SESSION & THREAD MAINTENANCE
# ******************************************

def add_thread(new_thread_id):
    if "chat_threads" not in st.session_state:
        st.session_state["chat_threads"] = []

    st.session_state["chat_threads"].append(new_thread_id)


if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())
    add_thread(st.session_state["thread_id"])


def reset_chat():
    st.session_state["thread_id"] = str(uuid.uuid4())
    add_thread(st.session_state["thread_id"])
    st.session_state["message_history"] = []


# ******************************************
# SIDE BAR
# ******************************************

st.sidebar.title("My conversations")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("Chat history")


# ******************************************
# PREVIOUS CHAT HISTORY
# ******************************************

def previous_chat_history(threadID):

    state = execute.get_state(
    config={"configurable": {"thread_id": threadID}}
    ).values

    previous_chat_history_lst = state.get("messages", [])

    clean_previous_chat_history_lst = []

    for i in previous_chat_history_lst:

        temp_dict = {}
        temp_dict["content"] = i.content

        if isinstance(i, AIMessage):
            temp_dict["avatar"] = "🤖"
            temp_dict["role"] = "ai"
        else:
            temp_dict["avatar"] = "👤"
            temp_dict["role"] = "user"

        clean_previous_chat_history_lst.append(temp_dict)

    return clean_previous_chat_history_lst


# ******************************************
# THREAD BUTTONS
# ******************************************

for thread in st.session_state["chat_threads"]:

    if st.sidebar.button(thread):

        # Make clicked thread the active thread
        st.session_state["thread_id"] = thread

        # Load messages of clicked thread
        st.session_state["message_history"] = previous_chat_history(thread)


# ******************************************
# DISPLAY CURRENT CHAT
# ******************************************

config = {
    "configurable": {
        "thread_id": st.session_state["thread_id"]
    }
}

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

else:
    for i in st.session_state["message_history"]:

        with st.chat_message(
            i["role"],
            avatar=i["avatar"]
        ):
            st.text(i["content"])


# ******************************************
# USER INPUT
# ******************************************

user_input = st.chat_input("Type here")


if user_input:

    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input,
        "avatar": "👤"
    })

    with st.chat_message("user", avatar="👤"):
        st.text(user_input)

    with st.chat_message("ai", avatar="🤖"):

        user_message = {
            "messages": user_input
        }

        ai_stream_response = execute.stream(
            user_message,
            config=config,
            stream_mode="messages"
        )

        ai_response = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in ai_stream_response
        )

    st.session_state["message_history"].append({
        "role": "ai",
        "content": ai_response,
        "avatar": "🤖"
    })