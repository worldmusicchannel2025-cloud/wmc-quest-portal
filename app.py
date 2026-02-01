import streamlit as st
import requests
from fpdf import FPDF

# --- CONFIGURATION & LINKS ---
MODEL_ID = "gemini-2.5-flash"
YOUTUBE_URL = "https://www.youtube.com/@WorldMusicChannel-y3s"
HOMEPAGE_URL = "https://world-music-channel-staging.b12sites.com/index"
SHOP_URL = "https://ko-fi.com/worldmusicchannel/shop"
DONATE_URL = "https://ko-fi.com/worldmusicchannel/goal?g=1"
CONTACT_EMAIL = "info@worldmusicchannel.com"

# --- CI-CONFORM PDF GENERATOR ---
class WMCPDF(FPDF):
    def header(self):
        try:
            self.image('logo.png', 10, 10, 25)
        except:
            pass
        self.set_y(15)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, 'World Music Channel', 0, 1, 'R')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, 'Official Lyric Interpretation', 0, 1, 'R')
        self.set_draw_color(200, 200, 200)
        self.line(10, 38, 200, 38)
        self.ln(20)

    def footer(self):
        self.set_y(-25)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)
        self.set_font('Arial', '', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, f'Contact: {CONTACT_EMAIL}', 0, 0, 'L')
        self.set_text_color(0, 0, 255)
        self.cell(0, 5, 'YouTube: @WorldMusicChannel-y3s', 0, 1, 'R', link=YOUTUBE_URL)
        self.set_text_color(100, 100, 100)
        self.set_x(10)
        self.cell(0, 5, f'Web: {HOMEPAGE_URL}', 0, 0, 'L')
        self.cell(0, 5, f'Page {self.page_no()}', 0, 0, 'R')

def create_pdf(text, session_name):
    pdf = WMCPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Session: {session_name}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", size=11)
    # Filter non-latin1 characters to prevent PDF crashes
    safe_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, safe_text)
    return pdf.output(dest='S').encode('latin-1')

# --- UI DESIGN ---
st.set_page_config(page_title="WMC Artist Portal", layout="centered")

col_info, col_logo = st.columns([3, 1])
with col_info:
    st.title("World Music Channel")
    st.markdown("### *Feel the Music*")
    st.caption("Official Artist Portal | Digital Muse 2.5")
    st.markdown("**INTERACTIVE EXPERIENCE WMC-TOOL**")

with col_logo:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.header("🎵")

st.markdown("---")

# --- APP LOGIC ---
q_code = st.text_input("Enter Quest Code:").upper()

if q_code == "LYA-SESSION-2":
    st.success("✅ Connected: Lya Nights")
    # Limit input to ~150 words (approx 1000 chars)
    user_lyrics = st.text_area("Paste lyrics (Max 150 words):", height=150, max_chars=1200)
    
    if st.button("✨ Reveal Interpretation", type="primary"):
        word_count = len(user_lyrics.split())
        
        if word_count > 150:
            st.error(f"Limit exceeded! Please use max 150 words. Current: {word_count}")
        elif word_count < 3:
            st.warning("Please enter some lyrics first.")
        elif "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent?key={api_key}"
            
            with st.spinner("The Muse is interpreting..."):
                # Instructions to output in the same language as input
                prompt = (
                    f"Analyze these lyrics deeply but concisely (max 180 words). "
                    f"MANDATORY: Answer in the same language as the lyrics provided. "
                    f"Lyrics: {user_lyrics}"
                )
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                response = requests.post(url, json=payload)
                
                if response.status_code == 200:
                    answer = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.markdown("### 🔮 Interpretation")
                    st.info(answer)
                    
                    pdf_data = create_pdf(answer, "Lya Nights")
                    col_dl, col_yt = st.columns(2)
                    with col_dl:
                        st.download_button("📄 Download PDF", pdf_data, "WMC_Interpretation.pdf", "application/pdf")
                    with col_yt:
                        st.link_button("🎬 Official Video", YOUTUBE_URL)
                    st.balloons()
                else:
                    st.error("Connection failed. Check your API key or model availability.")

# --- FOOTER ---
st.markdown("---")
st.markdown("### 🛍️ Exclusive WMC Collection")
c1, c2, c3, c4 = st.columns(4)
with c1: st.link_button("🎧 HD WAV", SHOP_URL)
with c2: st.link_button("🎵 MP3", SHOP_URL)
with c3: st.link_button("🎬 Video", SHOP_URL)
with c4: st.link_button("👕 Merch", SHOP_URL)

st.markdown("---")
c_home, c_empty, c_donate = st.columns([2, 1, 2])
with c_home:
    st.link_button("🌐 Visit WMC Homepage", HOMEPAGE_URL)
with c_donate:
    st.link_button("❤️ DONATE", DONATE_URL)
