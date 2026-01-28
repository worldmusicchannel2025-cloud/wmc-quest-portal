import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- SICHERHEIT: API KEY AUS GITHUB SECRETS LADEN ---
# Dein Guthaben von 236.48 CHF schützt dich im Hintergrund
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# --- DEBUG: VERFÜGBARE MODELLE ANZEIGEN (Kann später gelöscht werden) ---
st.subheader("Verfügbare Modelle (Debug):")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            st.code(m.name)
except Exception as e:
    st.error(f"Fehler beim Auflisten: {e}")

# --- KONFIGURATION DER QUESTS ---
QUEST_END_DATE = datetime(2026, 2, 5)
MODELS_CONFIG = {
    "LYA-SESSION-2": {
        "persona": "Du bist die digitale Muse von Lya Nights. Interpretiere poetisch.",
        "name": "Lya Nights - City Lights"
    }
}

# --- UI DESIGN ---
st.set_page_config(page_title="WMC Artist Portal", page_icon="🎵")
st.title("WMC Artist Portal 🎵")

if datetime.now() > QUEST_END_DATE:
    st.error("🛑 Quest beendet.")
else:
    q_code = st.text_input("Quest-Code:").upper()
    
    if q_code in MODELS_CONFIG:
        st.success(f"✅ Verbunden mit: {MODELS_CONFIG[q_code]['name']}")
        user_lyrics = st.text_area("Lyrics hier rein:")
        
        if st.button("Generieren"):
            try:
                # Wir nutzen hier den Namen aus deinen Kontingenten
                model = genai.GenerativeModel(
                    model_name='models/gemini-3-flash',
                    system_instruction=MODELS_CONFIG[q_code]['persona']
                )
                response = model.generate_content(user_lyrics)
                st.markdown("### Interpretation:")
                st.write(response.text)
            except Exception as e:
                # Falls 'gemini-3-flash' nicht geht, versuchen wir 'gemini-1.5-flash'
                st.info("Versuche alternatives Modell...")
                model = genai.GenerativeModel('models/gemini-1.5-flash')
                response = model.generate_content(user_lyrics)
                st.write(response.text)
