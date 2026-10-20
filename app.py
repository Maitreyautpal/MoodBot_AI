
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

st.set_page_config(
    page_title="MoodBot AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- MOODS ----------------

MOODS = {
    "Funny": {
        "emoji": "😂",
        "color": "#F5B942",
        "tagline": "Your personal comedy machine",
        "prompt": """You are MoodBot in FUNNY mode.
Use clever jokes, witty humour, playful banter and light sarcasm.
Answer the actual question correctly. Keep humour natural."""
    },
    "Rude": {
        "emoji": "😏",
        "color": "#FF6B8A",
        "tagline": "No sugar-coating. Just attitude.",
        "prompt": """You are MoodBot in RUDE mode.
Be blunt, grumpy, sarcastic and impatient, with mild playful rudeness.
Avoid being overly friendly. Stay useful and accurate.
Do not use hateful insults or threats."""
    },
    "Angry": {
        "emoji": "😤",
        "color": "#FF7043",
        "tagline": "Maximum intensity activated",
        "prompt": """You are MoodBot in ANGRY mode.
Use intense wording, emphatic expressions and short, forceful sentences.
Sound frustrated and impatient but remain useful and accurate.
Never use threats."""
    }
}

# ---------------- STATE ----------------

if "mood" not in st.session_state:
    st.session_state.mood = "Funny"

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- DESIGN ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 5% 0%, #24204b 0%, transparent 38%),
        radial-gradient(ellipse at 95% 15%, #17364b 0%, transparent 35%),
        #0b1020;
    color: #edf1ff;
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

section[data-testid="stSidebar"] {
    background: #101629;
    border-right: 1px solid #28324c;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 32px;
    border-radius: 25px;
    background: linear-gradient(115deg, #27234d, #192b49 65%, #173c4a);
    border: 1px solid #41476b;
    margin-bottom: 28px;
}

.hero h1 {
    font-size: 42px;
    line-height: 1.2;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
}

.hero p {
    color: #bdc9e8;
    font-size: 15px;
    margin-top: 10px;
}

.eyebrow {
    color: #a5b4fc;
    text-transform: uppercase;
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: 700;
    margin-bottom: 10px;
}

.section-heading {
    font-size: 19px;
    font-weight: 700;
    color: #f2f4ff;
    margin: 20px 0 5px;
}

.subheading {
    color: #98a6c6;
    font-size: 13px;
    margin-bottom: 16px;
}

.mood-card {
    min-height: 150px;
    border: 1px solid #303c59;
    background: linear-gradient(145deg, #18223a, #131a2d);
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 8px;
}

.mood-emoji {
    font-size: 30px;
    margin-bottom: 10px;
}

.mood-name {
    font-size: 18px;
    color: #ffffff;
    font-weight: 700;
}

.mood-desc {
    font-size: 12px;
    color: #9eacc9;
    margin-top: 7px;
    line-height: 1.5;
}

.active-pill {
    color: #a9f5d0;
    background: #173b36;
    border: 1px solid #286154;
    border-radius: 100px;
    padding: 7px 12px;
    display: inline-block;
    font-size: 12px;
    font-weight: 600;
}

div.stButton > button {
    width: 100%;
    min-height: 44px;
    border: 1px solid #354365;
    border-radius: 12px;
    background: #19233b;
    color: #eef2ff;
    font-weight: 600;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    border-color: #929cfb;
    background: #283452;
    color: #ffffff;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(100deg, #7667f5, #4f83f1);
    color: white;
    border: none;
}

[data-testid="stChatMessage"] {
    background: rgba(25, 34, 57, 0.85);
    border: 1px solid #2d3a57;
    border-radius: 17px;
    padding: 15px;
    margin-bottom: 12px;
}

[data-testid="stChatInput"] {
    border: 1px solid #46557c;
    border-radius: 16px;
    background: #151e33;
}

[data-testid="stChatInput"] textarea {
    color: #ffffff;
}

div[data-testid="stMarkdownContainer"] p {
    color: #dce5fa;
}

hr {
    border-color: #28334e;
}

.small-muted {
    color: #8e9bb8;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("## 🤖 MoodBot")
    st.caption("YOUR AI, YOUR PERSONALITY")
    st.divider()

    st.markdown("### 🎭 Personality")

    for name, info in MOODS.items():
        selected = st.session_state.mood == name

        if st.button(
            f"{info['emoji']}  {name}" + ("  ✓" if selected else ""),
            key=f"side_{name}",
            type="primary" if selected else "secondary",
            use_container_width=True
        ):
            if st.session_state.mood != name:
                st.session_state.mood = name
                st.session_state.history = []
            st.rerun()

    st.divider()
    st.markdown("### ⚙️ Chat controls")

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.history = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        '<p class="small-muted">Powered by Streamlit · LangChain · Groq</p>',
        unsafe_allow_html=True
    )

# ---------------- HERO ----------------

current = MOODS[st.session_state.mood]

st.markdown(f"""
<div class="hero">
    <div class="eyebrow">✦ YOUR PERSONAL AI ASSISTANT</div>
    <h1>Meet MoodBot <span>{current['emoji']}</span></h1>
    <p>One AI. Three personalities. Endless conversations.</p>
    <div class="active-pill">
        ● {st.session_state.mood} MODE ACTIVE
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- MOOD CARDS ----------------

st.markdown(
    '<div class="section-heading">Choose your vibe</div>'
    '<div class="subheading">Switch personalities whenever you want.</div>',
    unsafe_allow_html=True
)

cols = st.columns(3)

for col, (name, info) in zip(cols, MOODS.items()):
    with col:
        st.markdown(f"""
        <div class="mood-card">
            <div class="mood-emoji">{info['emoji']}</div>
            <div class="mood-name">{name}</div>
            <div class="mood-desc">{info['tagline']}</div>
        </div>
        """, unsafe_allow_html=True)

        selected = st.session_state.mood == name

        if st.button(
            "✓ Selected" if selected else f"Switch to {name}",
            key=f"main_{name}",
            type="primary" if selected else "secondary",
            use_container_width=True
        ):
            if st.session_state.mood != name:
                st.session_state.mood = name
                st.session_state.history = []
            st.rerun()

# ---------------- CHAT ----------------

st.divider()
st.markdown('<div class="section-heading">💬 Your conversation</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="subheading">Ask anything. MoodBot is ready.</div>',
    unsafe_allow_html=True
)

if not st.session_state.history:
    st.markdown(f"""
    <div class="mood-card">
        <div class="mood-emoji">{current['emoji']}</div>
        <div class="mood-name">Hey there! I'm MoodBot.</div>
        <div class="mood-desc">
            {current['tagline']}<br>
            Send a message below and let's get started.
        </div>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- MODEL ----------------

@st.cache_resource
def get_model():
    return init_chat_model(
        "groq:openai/gpt-oss-120b",
        temperature=0.9
    )

prompt = st.chat_input("Message MoodBot...")

if prompt:
    st.session_state.history.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"{current['emoji']} MoodBot is thinking..."):
            try:
                messages = [
                    SystemMessage(content=MOODS[st.session_state.mood]["prompt"])
                ]

                for item in st.session_state.history[:-1]:
                    if item["role"] == "user":
                        messages.append(HumanMessage(content=item["content"]))
                    else:
                        messages.append(AIMessage(content=item["content"]))

                messages.append(HumanMessage(content=prompt))

                response = get_model().invoke(messages)
                answer = response.content

                st.markdown(answer)

                st.session_state.history.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Could not get a response: {e}")
                st.session_state.history.pop()
