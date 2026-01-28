import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- KONFIGURATION ---
# Dein Guthaben von 236.48 CHF deckt die Nutzung sicher ab
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Fehler: API Key nicht gefunden. Bitte in Streamlit Secrets eintragen.")
    st.stop()

# --- QUEST EINSTELLUNGEN ---
QUEST_END_DATE = datetime(2026, 2, 15) 
MODELS_CONFIG = {
    "LYA-SESSION-2": {
        "persona": "Du bist die digitale Muse von Lya Nights. Dein Stil ist urban, poetisch und geheimnisvoll. Interpretiere die Songzeile tiefgründig.",
        "name": "Lya Nights - City Lights"
    }
}

# --- UI DESIGN ---
st.set_page_config(page_title="WMC Artist Portal", page_icon="🎵")
st.title("WMC Artist Portal 🎵")

# --- APP LOGIK ---
if datetime.now() > QUEST_END_DATE:
    st.error("🛑 Diese Quest ist leider beendet.")
else:
    q_code = st.text_input("Gib deinen Quest-Code aus dem Video ein:").upper()
    
    if q_code in MODELS_CONFIG:
        st.success(f"✅ Verbunden mit: {MODELS_CONFIG[q_code]['name']}")
        user_lyrics = st.text_area("Kopiere hier deine Lieblings-Lyrics rein:")
        
        if st.button("Artwork & Interpretation generieren"):
            with st.spinner("Die Muse verbindet sich..."):
                try:
                    # HIER IST DIE LÖSUNG: Wir nutzen exakt den Namen aus deiner Liste
                    model = genai.GenerativeModel(
                        model_name='models/gemini-2.0-flash', 
                        system_instruction=MODELS_CONFIG[q_code]['persona']
                    )
                    
                    response = model.generate_content(user_lyrics)
                    
                    st.markdown("### Deine persönliche Interpretation:")
                    st.write(response.text)
                    st.success("💡 Tipp: Poste das als Kommentar unter das Video!")
                    
                except Exception as e:
                    st.error(f"Ein technischer Fehler ist aufgetreten: {e}")
                    
    elif q_code != "":
        st.warning("Ungültiger Code. Hast du das Video bis zum Ende geschaut?")
