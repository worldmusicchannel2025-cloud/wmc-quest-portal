import streamlit as st
import requests

# --- CONFIG ---
YOUTUBE_URL = "https://www.youtube.com/@WorldMusicChannel-y3s"

# --- UI DESIGN (Logo oben Rechts) ---
st.set_page_config(page_title="WMC Artist Portal", layout="centered")

col1, col2 = st.columns([3, 1])
with col1:
    st.title("World Music Channel")
    st.markdown("### *Feel the Music*")
with col2:
    try: st.image("logo.png", width=120)
    except: st.write("🎵")

st.markdown("---")

# --- LOGIK ---
q_code = st.text_input("Quest Code:").upper()
if q_code == "LYA-SESSION-2":
    lyrics = st.text_area("Paste lyrics here:")
    if st.button("Reveal Interpretation", type="primary"):
        if "GEMINI_API_KEY" in st.secrets:
            # Stabiler v1 Endpunkt für 2026
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={st.secrets['GEMINI_API_KEY']}"
            res = requests.post(url, json={"contents": [{"parts": [{"text": lyrics}]}]})
            if res.status_code == 200:
                st.info(res.json()['candidates'][0]['content']['parts'][0]['text'])
            else:
                st.error(f"Verbindung steht, aber Google meldet Fehler: {res.status_code}")
        else:
            st.error("API Key fehlt in den Secrets!")

# --- SHOP FOOTER ---
st.markdown("---")
cols = st.columns(4)
links = ["HD WAV", "MP3", "Video", "Merch"]
for i, col in enumerate(cols):
    col.button(links[i], use_container_width=True)
