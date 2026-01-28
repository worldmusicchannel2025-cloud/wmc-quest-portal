import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- DEINE LINKS (BITTE HIER EINTRAGEN!) ---
# Kopiere hier die echten Links zu deinen Seiten rein:
YOUTUBE_VIDEO_URL = "https://www.youtube.com/channel/DEIN_KANAL_ODER_VIDEO_LINK" 
HOMEPAGE_URL = "https://www.worldmusicchannel.com"  # Deine Homepage
SHOP_URL = "https://www.worldmusicchannel.com/shop" # Dein Shop oder Merch-Link

# --- KONFIGURATION ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Error: API Key not found. Please check Streamlit Secrets.")
    st.stop()

# --- QUEST EINSTELLUNGEN ---
QUEST_END_DATE = datetime(2026, 2, 15) 
MODELS_CONFIG = {
    "LYA-SESSION-2": {
        "persona": (
            "You are the digital muse of Lya Nights. Your style is urban, poetic, and mysterious. "
            "Interpret the song lyrics deeply. "
            "IMPORTANT: Always answer in the exact same language as the user's lyrics. "
            "If lyrics are English, answer in English. If Spanish, answer in Spanish."
        ),
        "name": "Lya Nights - City Lights"
    }
}

# --- UI DESIGN & BRANDING ---
st.set_page_config(page_title="WMC Artist Portal", page_icon="🎵")

# Logo (falls vorhanden)
try:
    st.image("logo.png", width=200) 
except:
    pass 

st.title("WMC Artist Portal 🎵")
st.subheader("World-Music-Channel") # Dein gewünschter Untertitel

# --- APP LOGIC ---
if datetime.now() > QUEST_END_DATE:
    st.error("🛑 This quest has ended. Check back for the next video!")
    st.markdown(f"[Go back to World-Music-Channel]({HOMEPAGE_URL})")
else:
    # Story & Intro
    st.markdown("""
    ### ✨ Unlock the Soul of the Music
    Ready to see your favorite lyrics in a new light? 
    Our **AI Muse** will rewrite them into a unique, urban-poetic interpretation just for you.
    """)

    # Eingabe
    q_code = st.text_input("Enter the Quest Code from the video:").upper()
    
    if q_code in MODELS_CONFIG:
        st.success(f"✅ Connected to: {MODELS_CONFIG[q_code]['name']}")
        
        user_lyrics = st.text_area(
            "Paste your favorite lyrics here (max 300 chars):",
            max_chars=300,
            height=150,
            placeholder="e.g., 'Neon lights reflect in the rain of the night...'"
        )
        
        if st.button("✨ Reveal Interpretation"):
            if len(user_lyrics) < 10:
                st.warning("⚠️ Please enter at least a few words.")
            else:
                with st.spinner("The Muse is connecting..."):
                    try:
                        model = genai.GenerativeModel(
                            model_name='models/gemini-2.0-flash', 
                            system_instruction=MODELS_CONFIG[q_code]['persona']
                        )
                        response = model.generate_content(user_lyrics)
                        
                        # --- ERGEBNIS ANZEIGE ---
                        st.markdown("### 🔮 Your Personal Interpretation:")
                        st.info("👇 Copy this text below!")
                        st.code(response.text, language=None) # Code-Block macht das Kopieren leichter
                        
                        # --- CALL TO ACTION (ZURÜCK ZU YOUTUBE) ---
                        st.markdown("#### 🎁 Win the Contest!")
                        st.markdown("1. Copy the text above.")
                        st.markdown(f"2. **[Click here to paste it in the YouTube Comments!]({YOUTUBE_VIDEO_URL})**")
                        st.link_button("Go to YouTube Video 🎬", YOUTUBE_VIDEO_URL)
                        
                    except Exception as e:
                        st.error(f"Technical error: {e}")
    
    elif q_code != "":
        st.warning("Invalid Code. Did you watch the video until the end?")

    # --- FOOTER: WERBUNG & MERCH (IMMER SICHTBAR) ---
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 🌐 World-Music-Channel")
        st.markdown(f"Discover new artists and sounds on our official homepage.")
        st.markdown(f"[**Visit Homepage**]({HOMEPAGE_URL})")
        
    with col2:
        st.markdown(f"### 🛍️ Exclusive Fan Shop")
        st.markdown("Get limited HD WAV downloads, exclusive T-Shirts and Mugs!")
        st.markdown(f"[**Go to Shop**]({SHOP_URL})")
