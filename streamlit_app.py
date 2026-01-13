import streamlit as st
import pandas as pd
import re

# ---------------- CONFIG ----------------
st.set_page_config(page_title="FOXE ARENA", page_icon="🎵 ⚽️", layout="centered")

SHEET_ID = "1HBGfa4EygznWWdKk3CkcM-THGGsUDp6W"
SONGS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=wc-songs"

# ASSETS
LOGO = "https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/assets/IMG_9234.png"
ESTADIO = "https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/assets/8B390EC8-EB25-48F3-8838-76DE0F4416D9.png"

# ---------------- HELPERS ----------------
def get_video_id(url: str):
    if not isinstance(url, str): return None
    patterns = [r"youtu\.be\/([^?&]+)", r"youtube\.com\/watch\?v=([^?&]+)", r"youtube\.com\/shorts\/([^?&]+)"]
    for p in patterns:
        m = re.search(p, url)
        if m: return m.group(1)
    return None

def get_thumbnail(url: str) -> str:
    vid = get_video_id(url)
    return f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg" if vid else ""

@st.cache_data(ttl=30)
def load_songs():
    try:
        df = pd.read_csv(SONGS_URL)
        df.columns = [c.strip().lower() for c in df.columns]
        return df
    except: return pd.DataFrame()

# ---------------- CSS (LIMPIEZA Y AJUSTE DE ESPACIOS) ----------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');

/* OCULTAR ELEMENTOS DE STREAMLIT Y GITHUB */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}
button[title="View source on GitHub"] {{ display: none; }}

[data-testid="stAppViewContainer"] {{
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.8)), url("{ESTADIO}");
    background-size: cover;
    background-position: center;
}}

.block-container {{ 
    max-width: 450px; 
    padding-top: 1rem !important; 
    padding-bottom: 0rem !important;
}}

/* BIENVENIDA */
.welcome-container {{
    text-align: center;
    margin-bottom: 10px; /* Reducido para acercar a la música */
}}
.welcome-title {{
    font-size: 30px;
    font-weight: 900;
    color: #FFFFFF;
    text-transform: uppercase;
    margin-bottom: 5px;
}}
.welcome-title span {{
    color: #f5c542;
    text-shadow: 0 0 15px rgba(245,197,66,0.7);
}}
.welcome-subtitle {{
    font-size: 15px;
    color: rgba(255,255,255,0.85);
    font-weight: 300;
    line-height: 1.3;
}}
.welcome-subtitle b {{ color: #f5c542; font-weight: 600; }}

/* SECCIÓN MUSICA - ESPACIO ELIMINADO */
.music-header {{
    text-align: center;
    margin-top: 0px !important; /* Elimina espacio superior */
    padding-top: 10px;
}}
.music-icon {{
    color: #f5c542;
    font-size: 20px;
    margin-bottom: -5px; /* Acerca el icono al texto */
    filter: drop-shadow(0 0 5px #f5c542);
}}
.section-label {{
    font-size: 22px;
    font-weight: 800;
    color: #f5c542;
    letter-spacing: 1px;
    margin-top: 5px;
}}
.section-sub {{
    font-size: 11px;
    color: rgba(255,255,255,0.5);
    margin-top: -2px;
}}

/* CARD VIDEO */
.video-card {{
    background: rgba(20, 20, 20, 0.9);
    border: 1.5px solid #f5c542;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 15px;
    box-shadow: 0 0 30px rgba(245,197,66,0.2);
}}
.thumb-container {{ position: relative; width: 100%; aspect-ratio: 16/9; }}
.thumb-img {{ width: 100%; height: 100%; object-fit: cover; }}
.play-btn {{
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 55px; height: 55px;
    background: #ff0000;
    border-radius: 50%;
    display: flex; justify-content: center; align-items: center;
}}
.play-btn::after {{
    content: '';
    margin-left: 4px;
    border-left: 14px solid white;
    border-top: 10px solid transparent;
    border-bottom: 10px solid transparent;
}}
.video-info {{ padding: 15px 20px; }}
.v-title {{ font-size: 20px; font-weight: 700; color: #f5c542; }}
.v-sub {{ color: #ffffff; opacity: 0.9; font-size: 14px; margin-bottom: 8px; }}
.v-link {{ color: #f5c542 !important; font-size: 12px; text-decoration: underline !important; }}

/* FOOTER */
.footer-box {{ text-align: center; margin-top: 30px; padding-bottom: 20px; }}
.footer-logo {{ width: 40px; opacity: 0.9; margin-bottom: 5px; }}
.footer-text {{ font-size: 10px; color: rgba(255,255,255,0.3); }}
</style>
""", unsafe_allow_html=True)

# ---------------- ESTRUCTURA VISUAL ----------------

# 1. LOGO PRINCIPAL
st.markdown(f'<div style="text-align:center; margin-bottom:15px;"><img src="{LOGO}" width="160"></div>', unsafe_allow_html=True)

# 2. BIENVENIDA
st.markdown("""
<div class="welcome-container">
    <div class="welcome-title">¡BIENVENIDO A <span>FOXE ARENA</span>!</div>
    <div class="welcome-subtitle">
        Siente la pasión del mundial lo, haz tus pronósticos<br>
        y vibra con la <b>banda sonora oficial</b>.
    </div>
</div>
""", unsafe_allow_html=True)

# 3. SECCIÓN MÚSICA (ESPACIOS CORREGIDOS)
st.markdown("""
<div class="music-header">
    <div class="music-icon">♫</div>
    <div class="section-label">BANDA SONORA OFICIAL</div>
    <div class="section-sub">Las últimas canciones añadidas a la porra</div>
</div>
""", unsafe_allow_html=True)

# 4. CARD
songs = load_songs()
if not songs.empty:
    row = songs.iloc[0] 
    url = str(row.get('url', ''))
    st.markdown(f"""
    <div class="video-card">
        <a href="{url}" target="_blank" style="text-decoration:none;">
            <div class="thumb-container">
                <img class="thumb-img" src="{get_thumbnail(url)}">
                <div class="play-btn"></div>
            </div>
        </a>
        <div class="video-info">
            <div class="v-title">{row.get('nombre', 'Baila Baila')}</div>
            <div class="v-sub">{row.get('grupo', 'Himno Porra')}</div>
            <a class="v-link" href="{url}" target="_blank">Ver en YouTube</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 5. FOOTER
st.markdown(f"""
<div class="footer-box">
    <img src="{LOGO}" class="footer-logo"><br>
    <div class="footer-text">© 2026 FOXE ARENA. Todos los derechos reservados.</div>
</div>
""", unsafe_allow_html=True)
