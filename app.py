import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF

# --- CONFIG & LINKS ---
YOUTUBE_URL = "https://www.youtube.com/@WorldMusicChannel-y3s"
SHOP_LINKS = {
    "wav": "https://www.worldmusicchannel.com/shop/hd-wav",
    "mp3": "https://www.worldmusicchannel.com/shop/mp3",
    "video": "https://www.worldmusicchannel.com/shop/video",
    "merch": "https://www.worldmusicchannel.com/shop/merch"
}

# --- PDF GENERATOR ---
class WMCPDF(FPDF):
    def header(self):
        try: self.image('logo.png', 10, 10, 25)
        except: pass
        self.set_y(15)
        self.set_font('Arial', 'B', 15)
        self.cell(0, 8, 'World Music Channel', 0, 1, 'R')
        self.ln(15)

def create_pdf(text, name):
    pdf = WMCPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Interpretation: {name}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", size=11)
    safe_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, safe_text)
    return pdf.output(dest='S').encode('latin-1')

# --- ENGINE ---
def get_ai_response(prompt, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key.strip()}"
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        res = requests.post(url, json=data)
        if res.status_code == 200:
            return res.json()['candidates'][0]['content']['parts'][0]['text']
        return f"Fehler {res.status_code}: {res.text}"
    except Exception as e:
        return str(e)

# --- UI DESIGN (Logo oben Rechts) ---
st.set_page_config(page_title="WMC Artist Portal", page_icon="🎵")

col_info, col_logo = st.columns([2, 1])
with col_info:
    st.title("World Music Channel")
    st.markdown("### *Feel the Music*")
    st.caption("Official Artist Portal")
with col_logo:
    try: st.image("logo.png", use_container_width=True)
    except: st.header("🎵")

st.markdown("---")

# --- LOGIK ---
q_code = st.text_input("Quest Code:").upper()
if q_code == "LYA-SESSION-2":
    st.success("✅ Connected: Lya Nights")
    user_lyrics = st.text_area("Deine Lyrics:")
    if st.button("✨ Reveal Interpretation", type="primary"):
        if "GEMINI_API_KEY" in st.secrets:
            with st.spinner("Die Muse antwortet..."):
                resp = get_ai_response(user_lyrics, st.secrets["GEMINI_API_KEY"])
                st.info(resp)
                pdf = create_pdf(resp, "Lya Nights")
                st.download_button("📄 PDF Download", pdf, "WMC_Interpretation.pdf")
                st.link_button("🎬 Zum Video", YOUTUBE_URL)
        else: st.error("API Key fehlt!")

# --- FOOTER (Shop Buttons) ---
st.markdown("---")
st.markdown("### 🛍️ Exclusive WMC Collection")
c1, c2, c3, c4 = st.columns(4)
with c1: st.link_button("🎧 HD WAV", SHOP_LINKS["wav"])
with c2: st.link_button("🎵 MP3", SHOP_LINKS["mp3"])
with c3: st.link_button("🎬 Video", SHOP_LINKS["video"])
with c4: st.link_button("👕 Merch", SHOP_LINKS["merch"])
