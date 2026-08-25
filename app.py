import streamlit as st
from chatbot import get_response
from datetime import datetime
import time


# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Customer Support Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─── Premium CSS Theme ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Root Variables ── */
    :root {
        --bg-primary: #0b0f19;
        --bg-secondary: #111827;
        --bg-card: rgba(30, 41, 59, 0.5);
        --bg-sidebar: rgba(15, 23, 42, 0.85);
        --accent-1: #6366f1;
        --accent-2: #8b5cf6;
        --accent-3: #a78bfa;
        --gradient-primary: linear-gradient(135deg, #6366f1, #8b5cf6, #a78bfa);
        --gradient-glow: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --border-color: rgba(99, 102, 241, 0.15);
        --border-glow: rgba(99, 102, 241, 0.3);
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
        --shadow-glow: 0 0 20px rgba(99, 102, 241, 0.15);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
        --radius-full: 9999px;
        --transition-fast: 0.15s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-base: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ── Global ── */
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp {
        background: radial-gradient(ellipse at 20% 0%, rgba(99, 102, 241, 0.08) 0%, transparent 50%),
                    radial-gradient(ellipse at 80% 100%, rgba(139, 92, 246, 0.06) 0%, transparent 50%),
                    var(--bg-primary) !important;
    }

    /* ── Hide default Streamlit elements ── */
    #MainMenu, footer, header, [data-testid="stToolbar"] {
        display: none !important;
    }

    [data-testid="stDecoration"] {
        background: var(--gradient-primary) !important;
        height: 3px !important;
    }

    /* ── Custom Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(99, 102, 241, 0.3);
        border-radius: var(--radius-full);
    }
    ::-webkit-scrollbar-thumb:hover { background: rgba(99, 102, 241, 0.5); }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(11, 15, 25, 0.98) 100%) !important;
        border-right: 1px solid var(--border-color) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem !important;
    }

    /* ── Sidebar Expanders ── */
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background: rgba(30, 41, 59, 0.3) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        margin-bottom: 0.5rem !important;
        overflow: hidden !important;
        transition: all var(--transition-base) !important;
    }

    [data-testid="stSidebar"] [data-testid="stExpander"]:hover {
        border-color: var(--border-glow) !important;
        box-shadow: var(--shadow-glow) !important;
    }

    [data-testid="stSidebar"] [data-testid="stExpander"] summary {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.03em !important;
        text-transform: uppercase !important;
    }

    [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
        color: var(--accent-3) !important;
    }

    /* ── Sidebar Buttons ── */
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(99, 102, 241, 0.06) !important;
        color: var(--text-secondary) !important;
        border: 1px solid rgba(99, 102, 241, 0.1) !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.45rem 0.8rem !important;
        font-size: 0.82rem !important;
        font-weight: 400 !important;
        font-family: 'Inter', sans-serif !important;
        text-align: left !important;
        transition: all var(--transition-base) !important;
        margin-bottom: 0.25rem !important;
        cursor: pointer !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(99, 102, 241, 0.15) !important;
        color: var(--text-primary) !important;
        border-color: var(--accent-1) !important;
        box-shadow: 0 0 12px rgba(99, 102, 241, 0.2) !important;
        transform: translateX(3px) !important;
    }

    [data-testid="stSidebar"] .stButton > button:active {
        transform: translateX(3px) scale(0.98) !important;
    }

    /* ── Clear Chat Button (last button in sidebar) ── */
    .clear-chat-btn .stButton > button {
        background: rgba(239, 68, 68, 0.08) !important;
        color: #f87171 !important;
        border: 1px solid rgba(239, 68, 68, 0.2) !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 500 !important;
        transition: all var(--transition-base) !important;
    }

    .clear-chat-btn .stButton > button:hover {
        background: rgba(239, 68, 68, 0.18) !important;
        border-color: rgba(239, 68, 68, 0.4) !important;
        box-shadow: 0 0 16px rgba(239, 68, 68, 0.15) !important;
        transform: translateX(0px) !important;
    }

    /* ── Main Content ── */
    .main .block-container {
        max-width: 860px !important;
        padding: 2rem 1.5rem 6rem 1.5rem !important;
    }

    /* ── Chat Input ── */
    [data-testid="stChatInput"] {
        background: transparent !important;
    }

    [data-testid="stChatInput"] textarea {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-lg) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        padding: 0.8rem 1.2rem !important;
        transition: all var(--transition-base) !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        border-color: var(--accent-1) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.12), var(--shadow-glow) !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: var(--text-muted) !important;
    }

    [data-testid="stChatInput"] button {
        background: var(--gradient-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        transition: all var(--transition-base) !important;
    }

    [data-testid="stChatInput"] button:hover {
        box-shadow: var(--shadow-glow), 0 4px 12px rgba(99, 102, 241, 0.3) !important;
        transform: scale(1.05) !important;
    }

    /* ── Chat Messages ── */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        padding: 0.5rem 0 !important;
        animation: messageSlideIn 0.35s cubic-bezier(0.16, 1, 0.3, 1) both !important;
    }

    @keyframes messageSlideIn {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* ── User Message ── */
    [data-testid="stChatMessage"][data-testid-kind="user"] {
        flex-direction: row-reverse !important;
    }

    [data-testid="stChatMessage"][data-testid-kind="user"] > div:last-child {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.15)) !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        border-radius: var(--radius-lg) var(--radius-lg) 4px var(--radius-lg) !important;
        padding: 0.8rem 1.1rem !important;
        margin-left: 2rem !important;
    }

    /* ── Assistant Message ── */
    [data-testid="stChatMessage"][data-testid-kind="assistant"] > div:last-child {
        background: rgba(30, 41, 59, 0.4) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-lg) var(--radius-lg) var(--radius-lg) 4px !important;
        padding: 0.8rem 1.1rem !important;
        margin-right: 2rem !important;
        backdrop-filter: blur(10px) !important;
    }

    /* ── Avatar Styling ── */
    [data-testid="stChatMessage"] [data-testid="stAvatar"] {
        border-radius: var(--radius-full) !important;
        box-shadow: var(--shadow-sm) !important;
    }

    /* ── Markdown in Messages ── */
    [data-testid="stChatMessage"] .stMarkdown p {
        color: var(--text-primary) !important;
        font-size: 0.9rem !important;
        line-height: 1.7 !important;
    }

    /* ── Spinner / Loading ── */
    .stSpinner > div {
        border-top-color: var(--accent-1) !important;
    }

    [data-testid="stSpinnerTextContainer"] {
        color: var(--text-muted) !important;
        font-size: 0.82rem !important;
    }

    /* ── Divider ── */
    [data-testid="stSidebar"] hr {
        border-color: var(--border-color) !important;
        margin: 0.8rem 0 !important;
    }

    /* ── Generic text colors ── */
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown p {
        color: var(--text-primary) !important;
    }

    /* ── Timestamp styling ── */
    .msg-timestamp {
        font-size: 0.68rem;
        color: var(--text-muted);
        margin-top: 0.3rem;
        font-weight: 400;
        letter-spacing: 0.02em;
    }

    /* ── Welcome Card ── */
    .welcome-container {
        text-align: center;
        padding: 3rem 2rem;
        animation: welcomeFadeIn 0.7s ease-out both;
    }

    @keyframes welcomeFadeIn {
        from { opacity: 0; transform: translateY(20px) scale(0.97); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }

    .welcome-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        display: inline-block;
        animation: welcomePulse 2.5s ease-in-out infinite;
    }

    @keyframes welcomePulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.08); }
    }

    .welcome-title {
        font-size: 1.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, #f1f5f9, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }

    .welcome-subtitle {
        font-size: 0.92rem;
        color: var(--text-secondary);
        max-width: 480px;
        margin: 0 auto 2rem auto;
        line-height: 1.6;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.8rem;
        max-width: 520px;
        margin: 0 auto;
    }

    .feature-card {
        background: rgba(30, 41, 59, 0.35);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1rem;
        text-align: left;
        transition: all var(--transition-base);
    }

    .feature-card:hover {
        border-color: var(--border-glow);
        box-shadow: var(--shadow-glow);
        transform: translateY(-2px);
    }

    .feature-card-icon { font-size: 1.3rem; margin-bottom: 0.3rem; }
    .feature-card-title { font-size: 0.82rem; font-weight: 600; color: var(--text-primary); }
    .feature-card-desc { font-size: 0.72rem; color: var(--text-muted); margin-top: 0.15rem; }

    /* ── Sidebar Branding ── */
    .sidebar-brand {
        text-align: center;
        padding: 0.5rem 0 1rem 0;
    }

    .sidebar-brand-icon {
        font-size: 2rem;
        margin-bottom: 0.3rem;
        display: inline-block;
    }

    .sidebar-brand-title {
        font-size: 0.95rem;
        font-weight: 700;
        background: linear-gradient(135deg, #e2e8f0, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .sidebar-brand-sub {
        font-size: 0.68rem;
        color: var(--text-muted);
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-top: 0.1rem;
    }

    /* ── Typing Indicator ── */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 4px;
        padding: 0.4rem 0;
    }

    .typing-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--accent-1);
        animation: typingBounce 1.4s infinite ease-in-out;
        opacity: 0.6;
    }

    .typing-dot:nth-child(1) { animation-delay: 0s; }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }

    @keyframes typingBounce {
        0%, 80%, 100% { transform: scale(0.7); opacity: 0.4; }
        40% { transform: scale(1); opacity: 1; }
    }

    .typing-label {
        font-size: 0.75rem;
        color: var(--text-muted);
        margin-left: 6px;
        font-style: italic;
    }

    /* ── Status Indicator ── */
    .status-online {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        margin-top: 0.2rem;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #34d399;
        box-shadow: 0 0 8px rgba(52, 211, 153, 0.5);
        animation: statusPulse 2s ease-in-out infinite;
    }

    @keyframes statusPulse {
        0%, 100% { box-shadow: 0 0 4px rgba(52, 211, 153, 0.3); }
        50% { box-shadow: 0 0 12px rgba(52, 211, 153, 0.6); }
    }

    .status-text {
        font-size: 0.68rem;
        color: #34d399;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


# ─── Chat History Init ───────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []


# ─── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:

    # Brand header
    st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">🤖</div>
            <div class="sidebar-brand-title">Support Assistant</div>
            <div class="sidebar-brand-sub">Powered by Gemini AI</div>
            <div class="status-online">
                <div class="status-dot"></div>
                <span class="status-text">Online</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Account ──
    with st.expander("🔐  Account", expanded=False):
        if st.button("🔑  Reset Password", use_container_width=True, key="btn_pw"):
            st.session_state.selected_question = "How do I reset my password?"
        if st.button("📝  Create Account", use_container_width=True, key="btn_reg"):
            st.session_state.selected_question = "How do I create a new account?"

    # ── Orders ──
    with st.expander("📦  Orders", expanded=False):
        if st.button("📍  Track My Order", use_container_width=True, key="btn_track"):
            st.session_state.selected_question = "Where is my order?"
        if st.button("❌  Cancel Order", use_container_width=True, key="btn_cancel"):
            st.session_state.selected_question = "Can I cancel my order?"
        if st.button("🏠  Change Address", use_container_width=True, key="btn_addr"):
            st.session_state.selected_question = "How do I change my delivery address?"

    # ── Payments ──
    with st.expander("💳  Payments", expanded=False):
        if st.button("💰  Payment Methods", use_container_width=True, key="btn_pay"):
            st.session_state.selected_question = "What payment methods are accepted?"
        if st.button("⚠️  Payment Failed", use_container_width=True, key="btn_fail"):
            st.session_state.selected_question = "My payment failed."
        if st.button("🔄  Refund Policy", use_container_width=True, key="btn_refund"):
            st.session_state.selected_question = "What is your refund policy?"

    # ── Shipping ──
    with st.expander("🚚  Shipping", expanded=False):
        if st.button("⏱️  Shipping Time", use_container_width=True, key="btn_ship"):
            st.session_state.selected_question = "How long does shipping take?"
        if st.button("🌍  International Shipping", use_container_width=True, key="btn_intl"):
            st.session_state.selected_question = "Do you offer international shipping?"

    # ── Support ──
    with st.expander("🎧  Support", expanded=False):
        if st.button("📞  Contact Support", use_container_width=True, key="btn_contact"):
            st.session_state.selected_question = "How can I contact customer support?"
        if st.button("🧑‍💼  Human Agent", use_container_width=True, key="btn_human"):
            st.session_state.selected_question = "Can I talk to a human agent?"
        if st.button("📸  Damaged Product", use_container_width=True, key="btn_damage"):
            st.session_state.selected_question = "I received a damaged product."

    st.divider()

    # Clear conversation
    with st.container():
        st.markdown('<div class="clear-chat-btn">', unsafe_allow_html=True)
        if st.button("🗑️  Clear Conversation", use_container_width=True, key="btn_clear"):
            st.session_state.messages = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ─── Welcome Screen (when no messages) ───────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
        <div class="welcome-container">
            <div class="welcome-icon">💬</div>
            <div class="welcome-title">How can I help you today?</div>
            <div class="welcome-subtitle">
                I'm your AI-powered support assistant. Ask me anything about orders,
                payments, shipping, refunds, or your account.
            </div>
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-card-icon">📦</div>
                    <div class="feature-card-title">Order Tracking</div>
                    <div class="feature-card-desc">Track packages & manage orders</div>
                </div>
                <div class="feature-card">
                    <div class="feature-card-icon">💳</div>
                    <div class="feature-card-title">Payments</div>
                    <div class="feature-card-desc">Payment methods & issues</div>
                </div>
                <div class="feature-card">
                    <div class="feature-card-icon">🔄</div>
                    <div class="feature-card-title">Refunds</div>
                    <div class="feature-card-desc">Return policy & refund status</div>
                </div>
                <div class="feature-card">
                    <div class="feature-card-icon">🎧</div>
                    <div class="feature-card-title">Live Support</div>
                    <div class="feature-card-desc">Connect with a human agent</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ─── Display Previous Messages ────────────────────────────────────────────────────
for message in st.session_state.messages:

    with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])
        st.markdown(
            f'<div class="msg-timestamp">{message.get("timestamp", "")}</div>',
            unsafe_allow_html=True,
        )


# ─── User Input ──────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask me anything...")


# Check if a sidebar question was selected
if "selected_question" in st.session_state:
    user_input = st.session_state.selected_question
    del st.session_state.selected_question


# ─── Generate Response ────────────────────────────────────────────────────────────
if user_input:

    now = datetime.now().strftime("%I:%M %p")

    # Save old conversation before adding the new question
    chat_history = st.session_state.messages.copy()

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": now,
    })

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_input)
        st.markdown(f'<div class="msg-timestamp">{now}</div>', unsafe_allow_html=True)

    # Generate chatbot response
    with st.chat_message("assistant", avatar="🤖"):

        # Typing indicator
        typing_placeholder = st.empty()
        typing_placeholder.markdown("""
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <span class="typing-label">Thinking...</span>
            </div>
        """, unsafe_allow_html=True)

        response = get_response(user_input, chat_history)

        # Clear typing indicator and stream the response
        typing_placeholder.empty()

        # Stream the response word-by-word
        def stream_response():
            words = response.split(" ")
            for i, word in enumerate(words):
                yield word + (" " if i < len(words) - 1 else "")
                time.sleep(0.03)

        st.write_stream(stream_response)

        resp_time = datetime.now().strftime("%I:%M %p")
        st.markdown(
            f'<div class="msg-timestamp">{resp_time}</div>',
            unsafe_allow_html=True,
        )

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "timestamp": resp_time,
    })