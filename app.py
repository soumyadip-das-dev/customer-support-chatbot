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

# sidebar
with st.sidebar:

    st.header("Suggested Questions")

    st.markdown("### Account")

    if st.button("Reset Password", use_container_width=True):
        st.session_state.selected_question = "How do I reset my password?"

    if st.button("Create Account", use_container_width=True):
        st.session_state.selected_question = "How do I create an account?"

    st.markdown("### Orders")

    if st.button("Track Order", use_container_width=True):
        st.session_state.selected_question = "Where is my order?"

    if st.button("Cancel Order", use_container_width=True):
        st.session_state.selected_question = "Can I cancel my order?"

    if st.button("Change Address", use_container_width=True):
        st.session_state.selected_question = "How do I change my delivery address?"

    st.markdown("### Payments")

    if st.button("Payment Methods", use_container_width=True):
        st.session_state.selected_question = "What payment methods are accepted?"

    if st.button("Payment Failed", use_container_width=True):
        st.session_state.selected_question = "My payment failed."

    if st.button("Refund Policy", use_container_width=True):
        st.session_state.selected_question = "What is your refund policy?"

    st.markdown("### Shipping")

    if st.button("Shipping Time", use_container_width=True):
        st.session_state.selected_question = "How long does shipping take?"

    if st.button("International Shipping", use_container_width=True):
        st.session_state.selected_question = "Do you offer international shipping?"

    st.markdown("### Support")

    if st.button("Contact Support", use_container_width=True):
        st.session_state.selected_question = "How can I contact customer support?"

    if st.button("Human Agent", use_container_width=True):
        st.session_state.selected_question = "Can I talk to a human agent?"

    st.divider()

    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

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

            response = get_response(user_input)

            st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )