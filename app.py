import streamlit as st
import requests
from fpdf import FPDF
import qrcode
import os

# --- KONFIGURATION & LINKS ---
MODEL_ID = "gemini-2.5-flash"
YOUTUBE_URL = "https://www.youtube.com/@WorldMusicChannel-y3s"
HOMEPAGE_URL = "https://world-music-channel-staging.b12sites.com/index"
SHOP_URL = "https://ko-fi.com/worldmusicchannel/shop"
DONATE_URL = "https://ko-fi.com/worldmusicchannel/goal?g=1"
CONTACT_EMAIL = "info@worldmusicchannel.com"
QR_TARGET = YOUTUBE_URL 

# --- QR-CODE GENERATOR ---
QR_FILENAME = 'wmc_qr.png'
def generate_qr_code(url, filename):
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

if not os.path.exists(QR_FILENAME):
    generate_qr_code(QR_TARGET, QR_FILENAME)

# --- PDF GENERATOR ---
class WMCPDF(FPDF):
    def header(self):
        try: self.image('logo.png', 10, 10, 25)
        except: pass
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
        try: self.image(QR_FILENAME, 170, 265, 25)
        except: pass
        self.set_y(-30)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 165, self.get_y())
        self.ln(2)
        self.set_font('Arial', '', 8)
        self.set_text_color(100, 100, 100)
        self.set_x(10)
        self.cell(150, 5, f'Contact: {CONTACT_EMAIL}', 0, 1, 'L')
        self.set_x(10)
        self.cell(150, 5, f'Web: {HOMEPAGE_URL}', 0, 1, 'L')
        self.set_y(-30)
        self.set_x(165)
        self.set_text_color(0, 0, 255)
        self.cell(40, 5, 'Scan for YouTube ->', 0, 1, 'C', link=YOUTUBE_URL)
        self.set_x(165)
        self.set_text_color(100, 100, 100)
        self.cell(40, 5, f'Page {self.page_no()}', 0, 1, 'C')

def create_pdf(text, session_name):
    pdf = WMCPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Session: {session_name}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", size=11)
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
    user_lyrics = st.text_area("Paste lyrics (Max 150 words):", height
