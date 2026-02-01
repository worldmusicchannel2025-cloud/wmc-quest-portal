import streamlit as st
import requests
import json
from datetime import datetime
from fpdf import FPDF

# --- CONFIGURATION & LINKS ---
YOUTUBE_VIDEO_URL = "https://www.youtube.com/@WorldMusicChannel-y3s" 
HOMEPAGE_URL = "https://www.worldmusicchannel.com"
SHOP_LINKS = {
    "wav": "https://www.worldmusicchannel.com/shop/hd-wav",
    "mp3": "https://www.worldmusicchannel.com/shop/mp3",
    "video": "https://www.worldmusicchannel.com/shop/video",
    "merch": "https://www.worldmusicchannel.com/shop/merch"
}

QUEST_END_DATE = datetime(2026, 2, 15) 
MODELS_CONFIG = {
    "LYA-SESSION-2": {
        "persona": "You are the digital muse of Lya Nights. Interpret the lyrics deeply but concisely.",
        "name": "Lya Nights - City Lights"
    }
}

# --- PDF GENERATOR ---
class WMCPDF(FPDF):
    def header(self):
        try: self.image('logo.png', 10, 10, 30)
        except: pass 
        self.set_y(15)
        self.set_font('Arial', 'B', 16)
        self.cell(0, 8, 'World Music Channel', 0, 1, 'R')
        self.ln(10)

def create_corporate_pdf(text, name):
    pdf = WMCPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    safe_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, safe_text)
    return pdf.output(dest='S').encode('latin-1')

# --- INTELLIGENTE ENGINE (DIREKT-DIAGNOSE) ---
def get_gemini_response(prompt, api_key):
    clean_key = api_key.strip()
    
    # Liste der Modelle, die wir nacheinander probieren
    model_candidates = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-pro",
        "gemini-1.0-pro"
    ]
    
    last_error = ""
    
    for model_name in model_candidates:
        # Wir probieren erst v1 (stabiler), dann v1beta
        for version in ["v1", "v1beta"]:
            url = f"https://generativelanguage.googleapis.com/{version}/models/{model_name}:generateContent?key={clean_key}"
            data = {"contents": [{"parts": [{"text": prompt}]}]}
            
            try:
                response = requests.post(url, json=data, timeout=10)
                if response.status_code == 200:
                    return response.json()['candidates'][0]['content']['parts'][0]['text']
                else:
                    last_error = f"{model_name} ({version}): {response.status_code}"
            except Exception as e:
                last_error = str(e)
                
    return f"Diagnose-Fehler: Keines der Modelle konnte erreicht werden. Letzter Versuch war: {last_error}"

# --- UI DESIGN ---
st.set_page_config(page_title="WMC Artist Portal", page_icon="🎵", layout="centered")

col_text, col_img = st.columns([3, 1])
with col_text:
    st.title("World Music Channel")
    st.markdown("### *Feel the Music*") 
with col_img:
    try: st.image("logo.png", use_container_width=True)
    except: st.header("🎵") 

st.markdown("---")

if datetime.now() > QUEST_END_DATE:
    st.error("🛑 Quest ended.")
else:
    q_code = st.text_input("Enter Quest Code:").upper()
    
    if q_code in MODELS_CONFIG:
        st.success(f"✅ Connected: {MODELS_CONFIG[q_code]['name']}")
        user_lyrics = st.text_area("Paste lyrics:", height=100)
        
        if st.button("✨ Reveal Interpretation", type="primary"):
            if "GEMINI_API_KEY" not in st.secrets:
                st.error("⚠️ API Key fehlt!")
            else:
                with st.spinner("Die Muse sucht nach einem freien Kanal..."):
                    res = get_gemini_response(MODELS_CONFIG[q_code]['persona'] + "\n\n" + user_lyrics, st.secrets["GEMINI_API_KEY"])
                    
                    if "Diagnose-Fehler" in res:
                        st.error(res)
                        st.warning("Dein Schlüssel scheint für die API-Nutzung noch nicht aktiv zu sein. Bitte prüfe den Account-Typ im AI Studio.")
                    else:
                        st.info(res)
                        pdf = create_corporate_pdf(res, MODELS_CONFIG[q_code]['name'])
                        st.download_button("📄 Download PDF", pdf, "WMC_Interpretation.pdf", "application/pdf")

st.markdown("---")
c1, c2, c3, c4 = st.columns(4)
with c1: st.link_button("🎧 WAV", SHOP_LINKS["wav"])
with c2: st.link_button("🎵 MP3", SHOP_LINKS["mp3"])
with c3: st.link_button("🎬 Video", SHOP_LINKS["video"])
with c4: st.link_button("👕 Merch", SHOP_LINKS["merch"])
