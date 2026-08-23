import os
import uuid
import requests
import streamlit as st

st.set_page_config(
    page_title="Sherlock Holmes AI Detective",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling for Victorian/Detective Aesthetic
st.markdown(
    """
<style>
    /* Main Background and Text Colors */
    .stApp {
        background-color: #0F1419;
        color: #E2E8F0;
        font-family: 'Georgia', serif;
    }
    
    /* Title Banners */
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        border-bottom: 2px solid #D4AF37;
        margin-bottom: 2rem;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #F3E5AB;
        letter-spacing: 1px;
    }
    .main-subtitle {
        font-size: 1.1rem;
        color: #94A3B8;
        font-style: italic;
    }

    /* Example Query Buttons */
    .stButton>button {
        width: 100%;
        background-color: #1E293B;
        color: #F3E5AB;
        border: 1px solid #D4AF37;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #D4AF37;
        color: #0F1419;
        border-color: #F3E5AB;
    }

    /* Detective Investigation Loading Animation */
    .loading-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        padding: 1.5rem;
        background-color: #1E293B;
        border: 1px dashed #D4AF37;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .magnifier-pulse {
        font-size: 2.5rem;
        animation: pulse 1.5s infinite ease-in-out;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); opacity: 0.7; }
        50% { transform: scale(1.15); opacity: 1; }
        100% { transform: scale(0.95); opacity: 0.7; }
    }
    .loading-text {
        font-size: 1.1rem;
        color: #F3E5AB;
        font-weight: 600;
    }

    /* Chat Bubbles */
    .stChatMessage {
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


# Backend API & Session Management Configuration

# Pull backend URL from Streamlit Secrets or default local environment
if "API_BASE_URL" in st.secrets:
    API_BASE_URL = st.secrets["API_BASE_URL"].rstrip("/")
else:
    API_BASE_URL = os.getenv(
        "API_BASE_URL", "http://localhost:8000").rstrip("/")

# Automatic Session ID Generation & Storage
if "session_id" not in st.session_state:
    try:
        res = requests.get(f"{API_BASE_URL}/api/get_session_id", timeout=5)
        if res.status_code == 200:
            st.session_state.session_id = res.json().get("session_id")
        else:
            st.session_state.session_id = str(uuid.uuid4())
    except Exception:
        st.session_state.session_id = str(uuid.uuid4())

# Initialize chat history state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Greetings! I am Holmes' AI assistant, trained on the complete 62 canonical cases. What mystery or detail shall we investigate today?",
        }
    ]

# Sidebar UI (Metadata & Quick Stats)
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/c/cd/Sherlock_Holmes_Portrait_Paget.jpg",
        width='stretch',
        caption="Arthur Conan Doyle's Canon",
    )

    st.markdown("### 🔍 Case Files Overview")
    st.markdown(
        """
    - **Corpus:** 62 Sherlock Holmes Stories
    - **Architecture:** LangChain + Gemini Free LLM
    - **Vector Store:** Chroma Vector DB
    - **Backend:** Cloud FastAPI
    """
    )

    st.divider()

    # Session Status Indicator
    st.markdown(
        f"**Active Session:**\n`{st.session_state.session_id[:13]}...`"
    )

    if st.button("🧹 Clear Consultation History"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "The slate has been wiped clean. State your new inquiry.",
            }
        ]
        st.rerun()

# Main Interface & Layout
st.markdown(
    """
    <div class="main-header">
        <div class="main-title">🔍 Sherlock Holmes AI Detective</div>
        <div class="main-subtitle">"It is a capital mistake to theorize before one has data."</div>
    </div>
""",
    unsafe_allow_html=True,
)

# Suggested Starter Questions
st.markdown("#### 💡 Example Deductions to Request:")
col1, col2, col3 = st.columns(3)

prompt_to_send = None

with col1:
    if st.button(
        "🔎 What were the 3 features of the client in 'The Red-Headed League'?"
    ):
        prompt_to_send = "What were the three distinctive features of the client in 'The Red-Headed League'?"

with col2:
    if st.button("🎖️ Compare Dr. Watson's military background across stories."):
        prompt_to_send = (
            "Compare the military background of Dr. Watson across different stories."
        )

with col3:
    if st.button("⚖️ Cases where Holmes broke the law to solve a mystery?"):
        prompt_to_send = "List all cases where Sherlock Holmes was forced to break the law to solve the mystery."

# Chat Display Loop
for message in st.session_state.messages:
    avatar = "🕵️‍♂️" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat input bar
user_input = st.chat_input("Ask about any character, clue, or mystery...")

if user_input:
    prompt_to_send = user_input

# Query Execution & API Handler
if prompt_to_send:
    # Append user question to history
    st.session_state.messages.append(
        {"role": "user", "content": prompt_to_send}
    )
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt_to_send)

    # Process response with custom loading animation
    with st.chat_message("assistant", avatar="🕵️‍♂️"):
        loading_placeholder = st.empty()

        # Detective animated spinner
        loading_placeholder.markdown(
            """
            <div class="loading-container">
                <div class="magnifier-pulse">🕵️‍♂️🔍</div>
                <div class="loading-text">Examining 62 canonical texts & retrieving clues...</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        try:
            # Query FastAPI Cloud REST backend
            response = requests.post(
                f"{API_BASE_URL}/api/ask",
                json={
                    "session_id": st.session_state.session_id,
                    "question": prompt_to_send,
                },
                headers={"Content-Type": "application/json"},
                timeout=60,
            )

            loading_placeholder.empty()

            if response.status_code == 200:
                answer = response.json().get(
                    "answer", "No answer received from backend."
                )
            else:
                answer = f"⚠️ *Elementary Error:* Received status code `{response.status_code}` from the API."

        except requests.exceptions.Timeout:
            loading_placeholder.empty()
            answer = "⚠️ *The case took too long:* API timed out while scanning the vector embeddings."
        except Exception as e:
            loading_placeholder.empty()
            answer = (
                f"⚠️ *Connection Error:* Unable to connect to FastAPI cloud API at `{API_BASE_URL}`. Details: `{str(e)}`"
            )

        # Output final answer and record in session state
        st.markdown(answer)
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
