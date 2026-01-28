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
    safe_text = interpretation_text.encode('latin-1', 'replace
