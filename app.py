import streamlit as st
import requests
from fpdf import FPDF

# --- KONFIGURATION & LINKS ---
MODEL_ID = "gemini-2.5-flash"
YOUTUBE_URL = "https://www.youtube.com/@WorldMusicChannel-y3s"
HOMEPAGE_URL = "https://world-music-channel-staging.b12sites.com/index"
SHOP_URL = "https://ko-fi.com/worldmusicchannel/shop"
DONATE_URL = "https://ko-fi.com/worldmusicchannel/goal?g=1"

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
    # Entfernt Sonderzeichen, die latin-1 nicht mag
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
    st.markdown("**INTERACTIVE EXPERIENCE WMC-TOOL**")

with col_logo:
    try: st.image("logo.png", use_container_width=True)
    except: st.header("🎵")

st.markdown("---")

# --- APP LOGIK ---
q_code = st.text_input("Enter Quest Code:").upper()

if q_code == "LYA-SESSION-2":
    st.success("✅ Connected: Lya Nights")
    
    # Wort-Limit Hinweis (150 Wörter entsprechen ca. 1000 Zeichen)
    user_lyrics = st.text_area("Paste your lyrics here (Max 150 words):", height=150, max_chars=1000)
    
    if st.button("✨ Reveal Interpretation", type="primary"):
        # Wortzählung Check
        word_count = len(user_lyrics.split())
        if word_count > 150:
            st.error(f"Too many words! Please reduce to 150. (Current: {word_count})")
        elif word_count < 3:
            st.warning("Please enter some lyrics first.")
        elif "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent?key={api_key}"
            
            with st.spinner("The Muse is connecting to your soul..."):
                # Strenger Befehl für die Sprache
                prompt = (
                    f"Analyze and interpret these lyrics deeply but concisely (max 180 words). "
                    f"IMPORTANT: You MUST answer in the same language as the lyrics provided. "
                    f"Lyrics: {user_lyrics}"
                )
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                response = requests.post(url, json=payload)
                
                if response.status_code == 200:
                    answer = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.markdown("### 🔮 Interpretation")
                    st.info(answer)
                    
                    pdf_data = create_pdf(answer, "Lya Nights Session")
                    col_dl, col_yt = st.columns(2)
                    with col_dl:
                        st.download_button("📄 Download PDF", pdf_data, "WMC_Interpretation.pdf", "application/pdf")
                    with col_yt:
                        st.link_button("🎬 Official Video", YOUTUBE_URL)
                    st.balloons()
                else:
                    st.error("Connection error. Please try again.")

# --- FOOTER & SHOP LINKS ---
st.markdown("---")
st.markdown("### 🛍️ Exclusive WMC Collection")

# Erste Reihe: Shop Links
c1, c2, c3, c4 = st.columns(4)
with c1: st.link_button("🎧 HD WAV", SHOP_URL)
with c2: st.link_button("🎵 MP3", SHOP_URL)
with c3: st.link_button("🎬 Video", SHOP_URL)
with c4: st.link_button("👕 Merch", SHOP_URL)

st.markdown("---")
# Zweite Reihe: Homepage & Spende
c_home, c_empty, c_donate = st.columns([2, 1, 2])
with c_home:
    st.link_button("🌐 Visit WMC Homepage", HOMEPAGE_URL)
with c_donate:
    st.link_button("❤️ DONATE", DONATE_URL, type="secondary")
