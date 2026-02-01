import streamlit as st
import requests
from fpdf import FPDF
import qrcode
import os
import json
import base64
from datetime import datetime

# --- CONFIGURATION & LIMITS ---
MODEL_ID = "gemini-2.5-flash"
DAILY_LIMIT = 50 
USAGE_FILE = "usage_log.json"
YOUTUBE_URL = "https://www.youtube.com/@WorldMusicChannel-y3s"
HOMEPAGE_URL = "https://world-music-channel-staging.b12sites.com/index"
SHOP_URL = "https://ko-fi.com/worldmusicchannel/shop"
DONATE_URL = "https://ko-fi.com/worldmusicchannel/goal?g=1"
CONTACT_EMAIL = "world.music.channel2025@gmail.com"
QR_TARGET = YOUTUBE_URL 

# --- HELPER FUNCTIONS ---
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def get_usage_count():
    today = datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists(USAGE_FILE): return today, 0
    try:
        with open(USAGE_FILE, "r") as f:
            data = json.load(f)
            if data.get("date") == today: return today, data.get("count", 0)
    except: pass
    return today, 0

def increment_usage():
    today, count = get_usage_count()
    with open(USAGE_FILE, "w") as f:
        json.dump({"date": today, "count": count + 1}, f)

# --- QR-CODE GENERATOR ---
QR_FILENAME = 'wmc_qr.png'
if not os.path.exists(QR_FILENAME):
    qr = qrcode.make(QR_TARGET)
    qr.save(QR_FILENAME)

# --- PDF GENERATOR (UPDATED BRANDING) ---
class WMCPDF(FPDF):
    def header(self):
        try: self.image('logo.png', 10, 10, 25)
        except: pass
        self.set_y(15)
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'World Music Channel', 0, 1, 'R')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, 'Official Lyric Interpretation', 0, 1, 'R')
        self.set_draw_color(200, 200, 200); self.line(10, 38, 200, 38); self.ln(20)

    def footer(self):
        try: self.image(QR_FILENAME, 10, 265, 22)
        except: pass
        self.set_y(-30); self.set_draw_color(200, 200, 200); self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2); self.set_font('Arial', '', 8); self.set_text_color(100, 100, 100)
        self.set_x(35); self.cell(0, 5, f'Contact: {CONTACT_EMAIL}', 0, 1, 'L')
        self.set_x(35); self.cell(0, 5, f'Web: {HOMEPAGE_URL}', 0, 0, 'L')
        self.set_text_color(0, 0, 255); self.cell(0, 5, 'YouTube: @WorldMusicChannel-y3s', 0, 1, 'R', link=YOUTUBE_URL)

def create_pdf(text):
    pdf = WMCPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    # Updated text as per your request
    pdf.cell(0, 10, "World Music Channel - Free for Fans", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", size=11)
    safe_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, safe_text)
    return pdf.output(dest='S').encode('latin-1')

# --- UI DESIGN ---
st.set_page_config(page_title="WMC Artist Portal", layout="centered")

# CSS: Hides the GitHub icon, the Main Menu, and the "Deploy" button
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stAppDeployButton {display:none;}
            [data-testid="stToolbar"] {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

col_info, col_logo = st.columns([3, 1])
with col_info:
    st.title("World Music Channel")
    st.markdown("### *Feel the Music*")
    st.caption("Official Artist Portal | Digital Muse 2.5")
    st.markdown("**INTERACTIVE EXPERIENCE WMC-TOOL**")
    st.markdown("### *Official Lyric Interpretation*") 

with col_logo:
    try: st.image("logo.png", use_container_width=True)
    except: st.header("🎵")

st.markdown("---")

# --- APP LOGIC ---
q_code = st.text_input("Enter Quest Code:").upper()
today_date, current_usage = get_usage_count()
st.sidebar.title("WMC System")
st.sidebar.write(f"Daily Capacity: {current_usage} / {DAILY_LIMIT}")

if current_usage >= DAILY_LIMIT:
    st.error(f"🚨 Daily limit reached ({DAILY_LIMIT}/{DAILY_LIMIT}). The Muse is resting for today!")
else:
    # New simple Quest Code: WMC1
    if q_code == "WMC1":
        st.success("✅ Connected: World Music Session")
        user_lyrics = st.text_area("Paste lyrics (Max 150 words):", height=150, max_chars=1200)
        
        if st.button("✨ Reveal Interpretation", type="primary"):
            if len(user_lyrics.split()) > 150:
                st.error("Too many words!")
            elif len(user_lyrics.split()) < 3:
                st.warning("Please enter some lyrics.")
            elif "GEMINI_API_KEY" in st.secrets:
                api_key = st.secrets["GEMINI_API_KEY"]
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent?key={api_key}"
                with st.spinner("The Muse is thinking..."):
                    p = f"Interpret deeply in input language (max 180 words): {user_lyrics}"
                    res = requests.post(url, json={"contents": [{"parts": [{"text": p}]}]})
                    if res.status_code == 200:
                        answer = res.json()['candidates'][0]['content']['parts'][0]['text']
                        st.markdown("### 🔮 The Interpretation")
                        st.info(answer)
                        
                        increment_usage()
                        # Generates PDF with new title
                        pdf_data = create_pdf(answer)
                        col_dl, col_yt = st.columns(2)
                        with col_dl:
                            st.download_button("📄 Download PDF", pdf_data, "WMC_Interpretation.pdf")
                        with col_yt:
                            st.link_button("🎬 Official Video", YOUTUBE_URL)
                        st.balloons()
                    else:
                        st.error("API Connection Error. Please try again later.")
            else:
                st.error("Missing API Credentials in Secrets.")

# --- FOOTER ---
st.markdown("---")
st.markdown("### 🛍️ Exclusive WMC Collection")
c_sh = st.columns(4)
for i, txt in enumerate(["🎧 HD WAV", "🎵 MP3", "🎬 Video", "👕 Merch"]):
    with c_sh[i]: st.link_button(txt, SHOP_URL, use_container_width=True)

st.markdown("---")
c_home, c_qr, c_donate = st.columns([2, 1, 2])
with c_home:
    st.link_button("🌐 Visit Homepage", HOMEPAGE_URL, use_container_width=True)
    st.markdown(f"<p style='font-size: 0.8rem; color: gray;'>Contact: {CONTACT_EMAIL}</p>", unsafe_allow_html=True)
with c_qr:
    qr_b64 = get_image_base64(QR_FILENAME)
    if qr_b64:
        st.markdown(f'<div style="text-align: center;"><b>YouTube QR</b><br><img src="data:image/png;base64,{qr_b64}" width="100"></div>', unsafe_allow_html=True)
with c_donate:
    st.link_button("❤️ DONATE", DONATE_URL, type="primary", use_container_width=True)
