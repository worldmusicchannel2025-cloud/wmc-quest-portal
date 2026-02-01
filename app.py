import streamlit as st
import requests
from fpdf import FPDF

# --- KONFIGURATION & LINKS ---
MODEL_ID = "gemini-2.5-flash"
YOUTUBE_URL = "https://www.youtube.com/@WorldMusicChannel-y3s"
HOMEPAGE_URL = "https://world-music-channel-staging.b12sites.com/index"
SHOP_URL = "https://ko-fi.com/worldmusicchannel/shop"
DONATE_URL = "https://ko-fi.com/worldmusicchannel/goal?g=1"
CONTACT_EMAIL = "info@worldmusicchannel.com"  # Deine Email-Adresse

# --- PROFESSIONELLER PDF GENERATOR ---
class WMCPDF(FPDF):
    def header(self):
        # Logo
        try:
            self.image('logo.png', 10, 10, 25)
        except:
            pass
        
        # Header-Text rechts bündig
        self.set_font('Arial', 'B', 16)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, 'World Music Channel', 0, 1, 'R')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, 'Official Lyric Interpretation', 0, 1, 'R')
        
        # Trennlinie
        self.set_draw_color(200, 200, 200)
        self.line(10, 38, 200, 38)
        self.ln(20)

    def footer(self):
        # Position 2.5 cm von unten
        self.set_y(-25)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)
        
        self.set_font('Arial', '', 8)
        self.set_text_color(100, 100, 100)
        
        # Linke Seite: Email
        self.cell(0, 5, f'Contact: {CONTACT_EMAIL}', 0, 0, 'L')
        
        # Rechte Seite: YouTube Info
        # Klickbarer Link für Digital, ausgeschrieben für Analog
        self.set_text_color(0, 0, 255)
        self.cell(0, 5, 'Visit us on YouTube: @WorldMusicChannel-y3s', 0, 1, 'R', link=YOUTUBE_URL)
        
        self.set_text_color(100, 100, 100)
        self.set_x(10)
        self.cell(0, 5, f'Web: {HOMEPAGE_URL}', 0, 0, 'L')
        self.cell(0, 5, f'Page {self.page_no()}', 0, 0, 'R')

def create_pdf(text, session_name):
    pdf = WMCPDF()
    pdf.add_page()
    
    # Inhalt
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Session: {session_name}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", size=11)
    # Entfernt Sonderzeichen für latin-1 Kompatibilität
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
    try: st.image("logo.png", use_container_width=True)
    except: st.header("🎵")

st.markdown("---")

# --- APP LOGIK ---
q_code = st.text_input("Enter Quest Code:").upper()

if q_code == "LYA-SESSION-2":
    st.success("✅ Connected: Lya Nights")
    user_lyrics = st.text_area("Paste your lyrics here (Max 150 words):", height=150, max_chars=1000)
    
    if st.button("✨ Reveal Interpretation", type="primary"):
        word_count = len(user_lyrics.split())
        if word_count > 150:
