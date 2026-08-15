from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()
llm = ChatGroq(
    model="openai/gpt-oss-120b"
)
checkpointer = InMemorySaver()

# Define State
class message_state(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    
# Define Chat Function
def chat(state: message_state):
    history = state["messages"]
    response = llm.invoke(history)
    return {"messages":[response]}

# Define Graph
graph = StateGraph(message_state)

# Define Nodes
graph.add_node("chat",chat)

# Define Edges
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

# Compile Graph
execute = graph.compile(checkpointer=checkpointer)

# thread_id = "1"
# config = {"configurable":{"thread_id":thread_id}}


# while True:
#     user_input = input("Ask anything")
#     print("User: ",user_input)
#     if(user_input.strip().lower() in ["bye", "exit"]):
#         break
#     else:
#         latest_state = {"messages":[HumanMessage(content=user_input)]}
#         final_state = 
#         print(final_state["messages"][-1].content)        
        
