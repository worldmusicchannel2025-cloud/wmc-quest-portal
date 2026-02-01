import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF

# --- LINKS ---
YOUTUBE_URL = "https://www.youtube.com/@WorldMusicChannel-y3s"
SHOP_LINKS = {
    "wav": "https://www.worldmusicchannel.com/shop/hd-wav",
    "mp3": "https://www.worldmusicchannel.com/shop/mp3",
    "video": "https://www.worldmusicchannel.com/shop/video",
    "merch": "https://www.worldmusicchannel.com/shop/merch"
}

# --- UI DESIGN (Logo oben Rechts) ---
st.set_page_config(page_title="WMC Artist Portal", page_icon="🎵")

# Header: Info links, Logo rechts
col_info, col_logo = st.columns([2, 1])
with col_info:
    st.title("World Music Channel")
    st.markdown("### *Feel the Music*")
    st.caption("Official Artist Portal & Fan Experience. Unlock the hidden soul of your favorite lyrics.")

with col_logo:
    try:
        # Nutzt die logo.png aus deinem GitHub
        st.image("logo.png", use_container_width=True)
    except:
        st.header("🎵")

st.markdown("---")

# --- APP LOGIK ---
q_code = st.text_input("Enter Quest Code:").upper()

if q_code == "LYA-SESSION-2":
    st.success("✅ Connected: Lya Nights - City Lights")
    user_lyrics = st.text_area("Paste your favorite lyrics here:")
    
    if st.button("✨ Reveal Interpretation", type="primary"):
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            with st.spinner("The Muse is thinking..."):
                payload = {"contents": [{"parts": [{"text": user_lyrics}]}]}
                response = requests.post(url, json=payload)
                
                if response.status_code == 200:
                    answer = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.info(answer)
                else:
                    st.error(f"Error: {response.status_code}")
        else:
            st.error("API Key missing in Streamlit Secrets!")

# --- SHOP BUTTONS UNTEN ---
st.markdown("---")
st.markdown("### 🛍️ Exclusive WMC Collection")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.link_button("🎧 HD WAV", SHOP_LINKS["wav"])
with c2:
    st.link_button("🎵 MP3", SHOP_LINKS["mp3"])
with c3:
    st.link_button("🎬 Video", SHOP_LINKS["video"])
with c4:
    st.link_button("👕 Merch", SHOP_LINKS["merch"])
