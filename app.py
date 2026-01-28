import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- SICHERHEIT: API KEY AUS GITHUB SECRETS LADEN ---
# Wir nutzen dein Guthaben von 236.48 CHF sicher im Hintergrund
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# --- KONFIGURATION DER QUESTS ---
QUEST_END_DATE = datetime(2026, 2, 5) # Dein 7-Tage-Limit
MODELS = {
    "LYA-SESSION-2": {
        "persona": "Du bist die digitale Muse von Lya Nights. Dein Stil ist urban, geheimnisvoll und tiefgründig. Interpretiere die Songzeile poetisch und erstelle einen Bild-Prompt.",
        "name": "Lya Nights - City Lights"
    }
}

# --- UI DESIGN (WMC BRANDING) ---
st.set_page_config(page_title="WMC Artist Portal", page_icon="🎵")
st.title("WMC Artist Portal 🎵")

if datetime.now() > QUEST_END_DATE:
    st.error("🛑 Diese Quest ist leider beendet. Schau beim nächsten Video vorbei!")
else:
    q_code = st.text_input("Gib deinen Quest-Code aus dem Video ein:").upper()
    
    if q_code in MODELS:
        st.success(f"✅ Verbunden mit: {MODELS[q_code]['name']}")
        user_lyrics = st.text_area("Kopiere hier deine Lieblings-Lyrics rein:")
        
        if st.button("Artwork & Interpretation generieren"):
            # Wir nutzen das Gemini 3 Flash Modell für maximale Effizienz
            model = genai.GenerativeModel('gemini-3-flash', 
                                          system_instruction=MODELS[q_code]['persona'])
            response = model.generate_content(user_lyrics)
            
            st.markdown("### Deine persönliche Interpretation:")
            st.write(response.text)
            st.info("💡 Poste diesen Text als Kommentar unter das Video für deine Gewinnchance!")
    elif q_code != "":
        st.warning("Ungültiger Code. Schau dir das Video nochmal genau an!")
