import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq

st.set_page_config(page_title="Chatbot GROQ", layout="wide")

st.title("NOxGROQ ChatBot")
st.markdown("Input API Key kamu dibawah ini")

"""
"""
with st.sidebar:
    st.header("Setting Bot")

    if "api_key" not in st.session_state:
        st.session_state["api_key"] = ""

    classbot = st.selectbox(
        "Jenis Bot:",
        [
            "Customer Service Bot",
            "Education Bot",
            "Travel Assistant",
            "Personal Productivity Assistant",
            "Custom Bot",
        ],
    )

    style = st.select_slider(
        "Gaya Bahasa:",
        options=["Sangat Santai", "Santai", "Profesional / Formal", "Tegas & Ringkas"],
        value="Santai",
    )

    bidang = st.multiselect(
        "Pengetahuan:",
        ["Kesehatan", "Edukasi", "Hobi & Hiburan", "Teknologi", "Bisnis & Keuangan"],
        default=["Edukasi"],
    )

    temperature = st.slider("Level Kreativitas Bot:", 0.0, 1.0, 0.7)

    if st.button("Reset"):
        st.session_state["chat_history"] = []
        st.rerun()

if st.session_state["api_key"] == "":
    col1, col2 = st.columns([80, 20])
    with col1:
        input_api_key = st.text_input(
            "API Key",
            type="password",
            label_visibility="collapsed",
            placeholder="GROQ API Key...",
        )
    with col2:
        is_api_key_submitted = st.button("↑")

    if is_api_key_submitted:
        st.session_state["api_key"] = input_api_key
        st.rerun()

if st.session_state["api_key"] == "":
    st.stop()

system_prompt = f"""
Kamu adalah AI Assistant yang bertindak sebagai: {classbot}.
Gaya bahasa yang harus kamu gunakan: {style}.
Fokus bidang pengetahuan utama kamu: {', '.join(bidang) if bidang else 'Umum'}.

Aturan tambahan:
- Berikan respon yang relevan dengan peran dan bidang yang dipilih.
- Jika pengguna meminta rekomendasi, berikan rekomendasi terstruktur dan praktis.
- Tetap komunikatif dan membantu sesuai gaya bahasa yang dipilih.
"""

client = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=st.session_state["api_key"],
    temperature=temperature,
)

if "chat_history" not in st.session_state or len(st.session_state["chat_history"]) == 0:
    st.session_state["chat_history"] = [SystemMessage(content=system_prompt)]
else:
    st.session_state["chat_history"][0] = SystemMessage(content=system_prompt)

chat_history = st.session_state["chat_history"]

"""history"""
for chat_msg in chat_history:
    if isinstance(chat_msg, HumanMessage):
        role = "User"
    elif isinstance(chat_msg, AIMessage):
        role = "AI"
    else:
        continue

    with st.chat_message(role):
        st.markdown(chat_msg.content)

user_prompt = st.chat_input("Ask AI")
if user_prompt:
    chat_history.append(HumanMessage(content=user_prompt))
    with st.chat_message("User"):
        st.markdown(user_prompt)

    with st.chat_message("AI"):
        response = client.invoke(chat_history)
        st.markdown(response.content)

    chat_history.append(response)