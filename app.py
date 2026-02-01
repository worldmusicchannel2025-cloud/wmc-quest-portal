import streamlit as st
import requests

st.title("WMC - Muse Diagnostic")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("Key fehlt in Secrets!")
else:
    api_key = st.secrets["GEMINI_API_KEY"]
    
    # 1. Liste alle verfügbaren Modelle für DIESEN Key
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        response = requests.get(list_url)
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [m['name'] for m in models if 'generateContent' in m.get('supportedGenerationMethods', [])]
            
            if model_names:
                st.success(f"Gefundene Modelle: {model_names}")
                # Nutze das erste Modell in der Liste
                target = model_names[0]
                st.write(f"Nutze Modell: {target}")
                
                # Test-Anfrage
                gen_url = f"https://generativelanguage.googleapis.com/v1beta/{target}:generateContent?key={api_key}"
                res = requests.post(gen_url, json={"contents": [{"parts": [{"text": "Hello"}]}]})
                st.write("Antwort der Muse:", res.json()['candidates'][0]['content']['parts'][0]['text'])
            else:
                st.warning("Dein Key ist aktiv, aber Google gibt KEINE Modelle für dich frei. Prüfe die Regionaleinstellungen (Schweiz) im AI Studio.")
        else:
            st.error(f"Google Fehler {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Fehler: {str(e)}")
