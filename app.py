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

# Logo Integration (Bitte sicherstellen, dass 'logo.png' auf GitHub liegt)
try:
    st.image("logo.png", width=200) 
except:
    pass 

st.title("WMC Artist Portal 🎵")

# --- APP LOGIC ---
if datetime.now() > QUEST_END_DATE:
    st.error("🛑 This quest has ended. Check back for the next video!")
else:
    # Interface in English
    q_code = st.text_input("Enter the Quest Code from the video:").upper()
    
    if q_code in MODELS_CONFIG:
        st.success(f"✅ Connected to: {MODELS_CONFIG[q_code]['name']}")
        
        # --- DIE "STORY" (Einladender Text) ---
        st.markdown("""
        ### ✨ Unlock the Soul of the Music
        Ready to see your favorite lyrics in a new light? 
        
        Our **AI Muse** will analyze the deeper meaning behind the words and rewrite them 
        into a unique, urban-poetic interpretation just for you. 
        
        *Deep. Mysterious. Unique.*
        """)
        
        # Limit input to 300 characters (ca. 4-6 lines)
        user_lyrics = st.text_area(
            "Paste your favorite lyrics here (max 300 chars):",
            max_chars=300,
            height=150,
            placeholder="e.g., 'Neon lights reflect in the rain of the night...'"
        )
        
        if st.button("✨ Reveal Interpretation"):
            if len(user_lyrics) < 10:
                st.warning("⚠️ Please enter at least a few words to inspire the Muse.")
            else:
                with st.spinner("The Muse is connecting to the beat..."):
                    try:
                        model = genai.GenerativeModel(
                            model_name='models/gemini-2.0-flash', 
                            system_instruction=MODELS_CONFIG[q_code]['persona']
                        )
                        
                        response = model.generate_content(user_lyrics)
                        
                        st.markdown("### 🔮 Your Personal Interpretation:")
                        st.write(response.text)
                        
                        st.info("💡 **Winning Tip:** Copy the text above and post it as a comment under the YouTube video to enter the contest!")
                        
                    except Exception as e:
                        st.error(f"Technical error: {e}")
                    
    elif q_code != "":
        st.warning("Invalid Code. Did you watch the video until the end?")
