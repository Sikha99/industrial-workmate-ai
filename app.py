
import sys
from pathlib import Path

import streamlit as st

# Make the src folder accessible to Python
PROJECT_DIR = Path(__file__).resolve().parent
SRC_DIR = PROJECT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from orchestrator import process_request, resume_request
from answer_generator import FALLBACK


# Page configuration
st.set_page_config(
    page_title="Factory Work Assistant",
    page_icon="🏭",
    layout="centered"
)

st.title("🏭 Factory Work Assistant")
st.caption("AI-powered assistance for factory work management")
st.divider()

st.markdown(
    "Ask questions about factory rules or manage shifts "
    "using natural language."
)


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_request" not in st.session_state:
    st.session_state.pending_request = None


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def format_result(result):
    """Convert operation results into text for the chat."""
    if isinstance(result, dict):
        if result.get("status") == "missing_details":
            questions = result.get("questions", [])
            return questions[0] if questions else result.get(
                "message", "Please provide the missing details."
            )

        return result.get("answer", str(result))

    if result is None:
        return "The operation finished without returning a result."

    return str(result)


# Chat input
question = st.chat_input("Ask a factory-related question...")


if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Processing your request..."):
            try:
                # Continue the saved request, if one exists
                if st.session_state.pending_request is not None:
                    result = resume_request(
                        st.session_state.pending_request,
                        question
                    )
                else:
                    result = process_request(question)

                # Keep incomplete requests; clear them when finished
                if (
                    isinstance(result, dict)
                    and result.get("status") == "missing_details"
                ):
                    st.session_state.pending_request = result
                else:
                    st.session_state.pending_request = None

                answer = format_result(result)

                if not answer.strip():
                    answer = FALLBACK

                st.markdown(answer)

            except Exception as error:
                print("Application error:", error)
                answer = (
                    "Sorry, I couldn't process your request. "
                    "Check the terminal for the error details."
                )
                st.error(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# Sidebar
with st.sidebar:
    st.header("About")

    st.write(
        "An open-source factory assistant that answers questions "
        "from a local knowledge base and supports shift management."
    )

    st.caption("Local LLM: Qwen 2.5 1.5B")
    st.caption("Vector database: ChromaDB")
    st.caption("Embeddings: all-MiniLM-L6-v2")

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.session_state.pending_request = None
        st.rerun()
