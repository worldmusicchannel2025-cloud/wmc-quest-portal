import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF

# --- KONFIGURATION ---
MODEL_ID = "gemini-2.5-flash"  # Das Modell, das bei dir funktioniert hat!
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

# --- UI DESIGN ---
st.set_page_config(page_title="WMC Artist Portal", layout="centered")

# Header: Info links, Logo rechts
col_info, col_logo = st.columns([3, 1])
with col_info:
    st.title("World Music Channel")
    st.markdown("### *Feel the Music*")
    st.caption("Official Artist Portal | Digital Muse 2.5")
with col_logo:
    try: st.image("logo.png", use_container_width=True)
    except: st.header("🎵")

st.markdown("---")

# --- APP LOGIK ---
q_code = st.text_input("Enter Quest Code:").upper()

if q_code == "LYA-SESSION-2":
    st.success("✅ Connected: Lya Nights - City Lights")
    user_lyrics = st.text_area("Paste your lyrics here (max. 500 characters):", height=150)
    
    if st.button("✨ Reveal Interpretation", type="primary"):
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            # API-Aufruf mit dem funktionierenden 2.5-Modell
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent?key={api_key}"
            
            with st.spinner("The Muse is interpreting the soul of your lyrics..."):
                prompt = f"Interpret these lyrics deeply but concisely (max 200 words): {user_lyrics}"
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                
                response = requests.post(url, json=payload)
                
                if response.status_code == 200:
                    answer = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.markdown("### 🔮 The Muse says:")
                    st.info(answer)
                    
                    # PDF & Video Buttons
                    pdf_data = create_pdf(answer, "Lya Nights Session")
                    col_dl, col_yt = st.columns(2)
                    with col_dl:
                        st.download_button("📄 Download Interpretation (PDF)", pdf_data, "WMC_Interpretation.pdf", "application/pdf")
                    with col_yt:
                        st.link_button("🎬 Watch Official Video", YOUTUBE_URL)
                    st.balloons()
                else:
                    st.error(f"Error {response.status_code}: Please check your API settings.")
        else:
            st.error("API Key missing in Streamlit Secrets!")

# --- SHOP FOOTER ---
st.markdown("---")
st.markdown("### 🛍️ Exclusive WMC Collection")
c1, c2, c3, c4 = st.columns(4)
with c1: st.link_button("🎧 HD WAV", SHOP_LINKS["wav"])
with c2: st.link_button("🎵 MP3", SHOP_LINKS["mp3"])
with c3: st.link_button("🎬 Video", SHOP_LINKS["video"])
with c4: st.link_button("👕 Merch", SHOP_LINKS["merch"])
