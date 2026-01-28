import streamlit as st
import google.generativeai as genai

# --- DIAGNOSE MODUS ---
st.set_page_config(page_title="System Check", page_icon="🛠️")
st.title("🛠️ WMC System Diagnose")

# API Key laden
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    st.success("✅ API Key gefunden.")
except Exception as e:
    st.error(f"❌ API Key Fehler: {e}")
    st.stop()

# Modelle abfragen und anzeigen
st.subheader("Google hat diese Modelle für dich freigeschaltet:")
try:
    found_models = []
    for m in genai.list_models():
        # Wir suchen alles, was Inhalte generieren kann
        if 'generateContent' in m.supported_generation_methods:
            found_models.append(m.name)
            st.code(m.name)
            
    if not found_models:
        st.warning("⚠️ Keine Modelle gefunden. Prüfe API-Rechte.")
    else:
        st.success(f"✅ {len(found_models)} Modelle gefunden!")
        st.info("Bitte mache einen Screenshot von dieser Liste oder kopiere den Namen, der 'flash' enthält.")

except Exception as e:
    st.error(f"❌ Verbindungsfehler zu Google: {e}")
