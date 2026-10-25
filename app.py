
import sys
from pathlib import Path

import streamlit as st

# Locate the project root
PROJECT_DIR = Path(__file__).resolve().parent
SRC_DIR = PROJECT_DIR / "src"

# Make the src folder available for imports
sys.path.insert(0, str(SRC_DIR))

from answer_generator import answer_question, FALLBACK


# Configure the page
st.set_page_config(
    page_title="Factory Work Assistant",
    page_icon="🏭",
    layout="centered"
)

# Page heading
st.title("🏭 Factory Work Assistant")
st.caption("AI-powered assistance for factory work management")

st.divider()

st.markdown(
    "Ask questions about factory work procedures, "
    "worker assignments, training, departments, and skills."
)

# Keep the conversation during the current session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept a new question
question = st.chat_input("Ask a factory-related question...")

if question:
    # Display the user's question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Generate the answer
    with st.chat_message("assistant"):
        with st.spinner("Checking factory information..."):
            try:
                answer = answer_question(question)

                # Support the string return type used by the current pipeline
                if isinstance(answer, dict):
                    answer = answer.get("answer", FALLBACK)

                if not isinstance(answer, str) or not answer.strip():
                    answer = FALLBACK

                st.markdown(answer)

            except Exception:
                answer = (
                    "Sorry, I couldn't process your question. "
                    "Please try again."
                )
                st.error(answer)

    # Save the answer in the conversation
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

# Sidebar
with st.sidebar:
    st.header("About")
    st.write(
        "This application uses Retrieval-Augmented Generation (RAG) "
        "to answer questions using a local factory knowledge base."
    )

    st.caption("Local LLM: Qwen 2.5 1.5B")
    st.caption("Vector database: ChromaDB")
    st.caption("Embeddings: all-MiniLM-L6-v2")

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()
