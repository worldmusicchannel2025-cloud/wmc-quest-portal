import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURATION ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Error: API Key not found. Please check Streamlit Secrets.")
    st.stop()

# --- QUEST SETTINGS ---
QUEST_END_DATE = datetime(2026, 2, 15) 
MODELS_CONFIG = {
    "LYA-SESSION-2": {
        # System Instruction: AI will adapt to the input language automatically
        "persona": (
            "You are the digital muse of Lya Nights. Your style is urban, poetic, and mysterious. "
            "Interpret the song lyrics deeply. "
            "IMPORTANT: Always answer in the exact same language as the user's lyrics. "
            "If lyrics are English, answer in English. If Spanish, answer in Spanish."
        ),
        "name": "Lya Nights - City Lights"
    }
}

# --- UI DESIGN ---
st.set_page_config(page_title="WMC Artist Portal", page_icon="🎵")

# Logo Integration (Ensure 'logo.png' is uploaded to GitHub!)
# Falls du noch kein Logo hast, kannst du diese Zeile auskommentieren (# davor setzen)
try:
    st.image("logo.png", width=200) 
except:
    pass # Kein Fehler anzeigen, wenn Logo fehlt

st.title("WMC Artist Portal 🎵")
st.markdown("### Unlock your personal interpretation")

# --- APP LOGIC ---
if datetime.now() > QUEST_END_DATE:
    st.error("🛑 This quest has ended. Check back for the next video!")
else:
    # Interface in English
    q_code = st.text_input("Enter the Quest Code from the video:").upper()
    
    if q_code in MODELS_CONFIG:
        st.success(f"✅ Connected to: {MODELS_CONFIG[q_code]['name']}")
        
        # Limit input to 400 characters to protect API usage
        user_lyrics = st.text_area(
            "Paste your favorite lyrics here (max 400 chars):",
            max_chars=400,
            height=150
        )
        
        if st.button("Generate Interpretation"):
            if len(user_lyrics) < 10:
                st.warning("⚠️ Please enter at least a few words of lyrics.")
            else:
                with st.spinner("The Muse is connecting..."):
                    try:
                        model = genai.GenerativeModel(
                            model_name='models/gemini-2.0-flash', 
                            system_instruction=MODELS_CONFIG[q_code]['persona']
                        )
                        
                        response = model.generate_content(user_lyrics)
                        
                        st.markdown("### Your Personal Interpretation:")
                        st.write(response.text)
                        st.success("💡 Tip: Copy this text and post it as a comment under the YouTube video to win!")
                        
                    except Exception as e:
                        st.error(f"Technical error: {e}")
                    
    elif q_code != "":
        st.warning("Invalid Code. Did you watch the video until the end?")
