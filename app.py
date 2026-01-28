
import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- SICHERHEIT: API KEY AUS GITHUB SECRETS LADEN ---
# Wir nutzen dein Guthaben von 236.48 CHF sicher im Hintergrund
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# --- DEBUG: VERFÜGBARE MODELLE ANZEIGEN ---
# Dieser Teil hilft uns zu sehen, ob die Verbindung steht
st.subheader("Verfügbare Modelle (Debug):")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            st.code(m.name)
except Exception as e:
    st.error(f"Fehler beim Auflisten der Modelle: {e}")

# --- KONFIGURATION DER QUESTS ---
QUEST_END_DATE = datetime(2026, 2, 5) # Dein 7-Tage-Limit
MODELS_CONFIG = {
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
    
    if q_code in MODELS_CONFIG:
        st.success(f"✅ Verbunden mit: {MODELS_CONFIG[q_code]['name']}")
        user_lyrics = st.text_area("Kopiere hier deine Lieblings-Lyrics rein:")
        
        if st.button("Artwork & Interpretation generieren"):
            # Korrigierte Syntax für das Modell
            try:
                model = genai.GenerativeModel(
                    model_name='models/gemini-1.5-flash',
                    system_instruction=MODELS_CONFIG[q_code]['persona']
                )
                response = model.generate_content(user_lyrics)
                
                st.markdown("### Deine persönliche Interpretation:")
                st.write(response.text)
                st.info("💡 Poste diesen Text als Kommentar unter das Video für deine Gewinnchance!")
            except Exception as e:
                st.error(f"Fehler bei der KI-Anfrage: {e}")
                
    elif q_code != "":
        st.warning("Ungültiger Code. Schau dir das Video nochmal genau an!")
