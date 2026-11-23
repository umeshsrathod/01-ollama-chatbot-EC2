
import streamlit as st
from backend import ask_ollama

# Application configuration
st.set_page_config(page_title="Ollama AI Chatbot")

# Application heading
st.title("Ollama AI Chatbot")

st.write("Chat with your local Llama model")

# Maintain conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous conversation
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# Get user input
user_question = st.chat_input("Ask me anything...")

if user_question:

    # Add user question to history
    st.session_state.messages.append(
        {"role": "user", "content": user_question}
    )

    # Display user question
    with st.chat_message("user"):
        st.write(user_question)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("AI is thinking..."):

            answer = ask_ollama(
                st.session_state.messages
            )

            st.write(answer)

    # Save AI response
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
