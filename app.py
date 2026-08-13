import streamlit as st
from chatbot import get_response

# page settings
st.set_page_config(
    page_title="Customer Support Chatbot",
    layout="wide"
)

# title
st.title("Customer Support Chatbot")
st.caption("Ask questions related to orders, payments, refunds and account support.")

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# user input
user_input = st.chat_input("Type your question...")

# if a sidebar question is clicked
if "selected_question" in st.session_state:

    user_input = st.session_state.selected_question
    del st.session_state.selected_question

# generate response
if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            response = get_response(user_input, st.session_state.messages)
            st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )