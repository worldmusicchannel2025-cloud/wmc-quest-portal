import streamlit as st
import google.generativeai as genai
from datetime import datetime
from fpdf import FPDF

# --- DEINE ECHTEN LINKS (BITTE HIER EINTRAGEN!) ---
YOUTUBE_VIDEO_URL = "https://www.youtube.com/@WorldMusicChannel" 
HOMEPAGE_URL = "https://www.worldmusicchannel.com"
SHOP_LINKS = {
    "wav": "https://www.worldmusicchannel.com/shop/hd-wav",
    "mp3": "https://www.worldmusicchannel.com/shop/mp3",
    "video": "https://www.worldmusicchannel.com/shop/video",
    "merch": "https://www.worldmusicchannel.com/shop/merch"
}

# --- PDF GENERATOR (CORPORATE DESIGN) ---
class WMCPDF(FPDF):
    def header(self):
        # Logo oben links (Position x=10, y=8, Breite=33mm)
        # Try-Except fängt ab, falls das Logo mal fehlt
        try:
            self.image('logo.png', 10, 8, 33)
        except:
            pass # Kein Logo, kein Drama
            
        self.set_font('Arial', 'B', 15)
        # Titel nach rechts verschieben (damit er nicht im Logo steht)
        self.cell(80) 
        self.cell(30, 10, 'World Music Channel', 0, 0, 'C')
        self.ln(20)
        # Linie ziehen (Corporate Style)
        self.set_line_width(0.5)
        self.line(10, 30, 200, 30)
        self.ln(10)

    def footer(self):
        # Position 1.5 cm von unten
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128) # Grau
        self.cell(0, 10, f'Page {self.page_no()} - Official WMC Artist Portal', 0, 0, 'C')

def create_corporate_pdf(interpretation_text, code_name):
    pdf = WMCPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Überschrift Quest
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0) # Schwarz
    pdf.cell(0, 10, f"Interpretation: {code_name}", ln=True, align='L')
    pdf.ln(5)
    
    # Der Text
    pdf.set_font("Arial", size=11)
    # Text bereinigen für PDF (Sonderzeichen-Schutz)
    safe_text = interpretation_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, safe_text)
    
    return pdf.output(dest='S').encode('latin-1')

# --- CONFIGURATION ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Error: API Key not found.")
    st.stop()

QUEST_END_DATE = datetime(2026, 2, 15) 
MODELS_CONFIG = {
    "LYA-SESSION-2": {
        "persona": (
            "You are the digital muse of Lya Nights. Interpret the lyrics deeply. "
            "IMPORTANT: Answer in the same language as the lyrics."
        ),
        "name": "Lya Nights - City Lights"
    }
}

# --- UI DESIGN ---
st.set_page_config(page_title="WMC Artist Portal", page_icon="🎵")

# Logo in der App
try:
    st.image("logo.png", width=200) 
except:
    pass

st.title("WMC Artist Portal 🎵")

# --- APP LOGIC ---
if datetime.now() > QUEST_END_DATE:
    st.error("🛑 Quest ended.")
    st.link_button("Go to Homepage", HOMEPAGE_URL)
else:
    st.markdown("""
    **Unlock the Soul of the Music.** Paste your lyrics below.
    """)

    q_code = st.text_input("Enter Quest Code:").upper()
    
    if q_code in MODELS_CONFIG:
        st.success(f"✅ Connected: {MODELS_CONFIG[q_code]['name']}")
        
        user_lyrics = st.text_area("Paste lyrics (max 300 chars):", max_chars=300, height=100)
        
        if st.button("✨ Reveal Interpretation"):
            if len(user_lyrics) > 5:
                with st.spinner("Processing..."):
                    try:
                        model = genai.GenerativeModel('models/gemini-2.0-flash', 
                                                      system_instruction=MODELS_CONFIG[q_code]['persona'])
                        response = model.generate_content(user_lyrics)
                        
                        # --- ERGEBNIS ---
                        st.markdown("---")
                        st.markdown("### 🔮 Your Personal Interpretation")
                        
                        # Schöne Info-Box für Lesbarkeit
                        st.info(response.text)
                        
                        # --- PDF DOWNLOAD (Corporate) ---
                        pdf_bytes = create_corporate_pdf(response.text, MODELS_CONFIG[q_code]['name'])
                        st.download_button(
                            label="📄 Download Official PDF (WMC Design)",
                            data=pdf_bytes,
                            file_name="WMC_Interpretation.pdf",
                            mime="application/pdf"
                        )
                        
                        # Copy Help
                        st.caption("👇 Click inside to copy for YouTube:")
                        st.text_area("Copy Text", value=response.text, height=100, label_visibility="collapsed")
                        st.link_button("Go to YouTube to Comment 🎬", YOUTUBE_VIDEO_URL)
                        
                    except Exception as e:
                        st.error(f"Error: {e}")
    elif q_code != "":
        st.warning("Invalid Code.")

# --- SHOP & FOOTER ---
st.markdown("---")
st.markdown("### 🛍️ Exclusive WMC Collection")

# 4 Shop Spalten
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("**🎧 HD WAV**")
    st.caption("Audiophile Quality")
    st.link_button("Go to Shop", SHOP_LINKS["wav"])

with c2:
    st.markdown("**🎵 MP3**")
    st.caption("Universal Format")
    st.link_button("Go to Shop", SHOP_LINKS["mp3"])

with c3:
    st.markdown("**🎬 Video**")
    st.caption("Official Cut")
    st.link_button("Go to Shop", SHOP_LINKS["video"])

with c4:
    st.markdown("**👕 Merch**")
    st.caption("Shirt & Mug")
    st.link_button("Go to Shop", SHOP_LINKS["merch"])

# --- HOMEPAGE LINK (GANZ UNTEN) ---
st.markdown("---")
st.markdown("### 🌐 Explore More")
# Zentrierter Button (Workaround mit Columns)
col_l, col_center, col_r = st.columns([1, 2, 1])
with col_center:
    st.link_button("🌐 Visit Official Homepage (World Music Channel)", HOMEPAGE_URL, use_container_width=True)
