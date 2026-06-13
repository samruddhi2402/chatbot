
import streamlit as st
from chatbot import get_response

# ------------------ Page Config ------------------ #

st.set_page_config(
    page_title="DevSupport AI",
    page_icon="🤖",
    layout="wide"
)

# ------------------ Load CSS ------------------ #

def load_css():
    try:
        with open("style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except:
        pass

load_css()

# ------------------ Session State ------------------ #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_code" not in st.session_state:
    st.session_state.uploaded_code = None

# ------------------ Sidebar ------------------ #

with st.sidebar:

    st.title("🤖 DevSupport AI")

    st.markdown("### AI Software Development Assistant")

    st.divider()

    uploaded_file = st.file_uploader(
        "📂 Upload Code File",
        type=["py", "java", "cpp", "c", "js", "html", "css", "sql", "txt"]
    )

    if uploaded_file is not None:

        st.session_state.uploaded_code = uploaded_file.read().decode("utf-8")

        st.success("✅ File Uploaded Successfully")

    use_uploaded_code = st.checkbox(
        "📄 Analyze Uploaded File",
        value=False
    )

    if st.button("➕ New Chat", use_container_width=True):

        st.session_state.messages = []
        st.session_state.uploaded_code = None

        st.rerun()

    st.divider()

    st.markdown("### 🚀 Features")

    st.markdown("""
- 💬 General Coding Chat
- 📄 Code Explanation
- 🐞 Bug Detection
- ⚡ Code Optimization
- 📚 DSA Assistance
- 🤖 AI & ML Guidance
""")



# ------------------ Main Page ------------------ #

st.title("🤖 DevSupport AI")

st.caption("Your Intelligent Software Development Assistant")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Model", "Gemini")

with col2:
    st.metric("Status", "🟢 Online")

with col3:
    st.metric("Version", "v1.0")

# ------------------ Welcome ------------------ #

if len(st.session_state.messages) == 0:

    st.markdown(
        """
        # 👋 Welcome to DevSupport AI

        Ask any software development or programming question using the chat box below.

        Start a conversation or upload a code file for analysis.
        """
    )

# ------------------ Uploaded Code ------------------ #

if st.session_state.uploaded_code:

    with st.expander("📄 Uploaded Code"):

        st.code(
            st.session_state.uploaded_code,
            language="python"
        )


# ------------------ Chat History ------------------ #

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# ------------------ Chat Input ------------------ #

prompt = st.chat_input("💬 Ask your coding question...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("🤖 Thinking..."):

            if use_uploaded_code and st.session_state.uploaded_code:

                response = get_response(
                    prompt,
                    st.session_state.uploaded_code
                )

            else:

                response = get_response(prompt)

            st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

# ------------------ Footer ------------------ #

st.divider()

st.markdown(
    """
    <div style="text-align:center;color:gray;">
    🚀 <b>DevSupport AI</b><br>
    Built with Python • Streamlit • Gemini API
    </div>
    """,
    unsafe_allow_html=True
)

