import streamlit as st
import pandas as pd
import re

# ---------------- CONFIG ----------------
st.set_page_config(page_title="FOXE ARENA", page_icon="🎵", layout="centered")

SHEET_ID = "1HBGfa4EygznWWdKk3CkcM-THGGsUDp6W"
SONGS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=wc-songs"
USERS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=wc-user"

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

# ---------------- CSS (MAQUETACIÓN DE ALTA CALIDAD) ----------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');

header {{ visibility: hidden; }}
[data-testid="stAppViewContainer"] {{
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.85)), url("{ESTADIO}");
    background-size: cover;
    background-position: center;
}}

.block-container {{ max-width: 450px; padding-top: 2rem; }}

/* TEXTO GLOW */
.welcome-container {{
    text-align: center;
    margin-bottom: 40px;
}}
.welcome-title {{
    font-size: 32px;
    font-weight: 900;
    color: #FFFFFF;
    text-transform: uppercase;
    margin-bottom: 10px;
}}
.welcome-title span {{
    color: #f5c542;
    text-shadow: 0 0 20px rgba(245,197,66,0.8);
}}
.welcome-subtitle {{
    font-size: 16px;
    color: rgba(255,255,255,0.8);
    font-weight: 300;
    line-height: 1.4;
}}
.welcome-subtitle b {{ color: #f5c542; font-weight: 600; }}

/* ICONOGRAFÍA SCROLL */
.scroll-icon {{
    margin: 30px auto;
    width: 24px;
    height: 40px;
    border: 2px solid #f5c542;
    border-radius: 12px;
    position: relative;
    box-shadow: 0 0 15px rgba(245,197,66,0.4);
}}
.scroll-icon::before {{
    content: '';
    position: absolute;
    left: 50%;
    top: 8px;
    transform: translateX(-50%);
    width: 4px;
    height: 8px;
    background: #f5c542;
    border-radius: 2px;
    animation: scroll-anim 2s infinite;
}}
@keyframes scroll-anim {{
    0% {{ opacity: 1; top: 8px; }}
    100% {{ opacity: 0; top: 20px; }}
}}

/* SECCIÓN MUSICA */
.music-header {{
    text-align: center;
    margin-top: 50px;
}}
.music-header img {{ width: 30px; margin-bottom: 10px; filter: drop-shadow(0 0 8px #f5c542); }}
.section-label {{
    font-size: 24px;
    font-weight: 800;
    color: #f5c542;
    letter-spacing: 2px;
}}

/* CARD VIDEO */
.video-card {{
    background: rgba(15, 15, 15, 0.85);
    border: 2px solid #f5c542;
    border-radius: 25px;
    padding: 0;
    overflow: hidden;
    margin-top: 20px;
    box-shadow: 0 0 40px rgba(245,197,66,0.25);
}}
.thumb-container {{ position: relative; width: 100%; aspect-ratio: 16/9; }}
.thumb-img {{ width: 100%; height: 100%; object-fit: cover; }}
.play-btn {{
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 60px; height: 60px;
    background: rgba(255,0,0,0.9);
    border-radius: 50%;
    display: flex; justify-content: center; align-items: center;
    box-shadow: 0 0 20px rgba(0,0,0,0.5);
}}
.play-btn::after {{
    content: '';
    margin-left: 5px;
    border-left: 15px solid white;
    border-top: 10px solid transparent;
    border-bottom: 10px solid transparent;
}}
.video-info {{ padding: 20px; }}
.v-title {{ font-size: 22px; font-weight: 700; color: #f5c542; margin-bottom: 5px; }}
.v-sub {{ color: #ffffff; opacity: 0.8; font-size: 14px; }}
.v-link {{ color: #f5c542 !important; font-size: 13px; text-decoration: none; display: block; margin-top: 10px; }}

/* FOOTER & ADMIN DISCRETO */
.footer-box {{ text-align: center; margin-top: 50px; padding-bottom: 40px; }}
.footer-logo {{ width: 50px; opacity: 0.8; margin-bottom: 10px; }}
.footer-text {{ font-size: 11px; color: rgba(255,255,255,0.4); }}

/* BOTON ADMIN DISCRETO */
.stButton>button {{
    background: transparent !important;
    border: 1px solid rgba(245,197,66,0.2) !important;
    color: rgba(255,255,255,0.3) !important;
    font-size: 10px !important;
    border-radius: 8px !important;
    padding: 2px 10px !important;
    width: auto !important;
    margin: 10px auto !important;
    display: block !important;
}}
.stButton>button:hover {{
    color: #f5c542 !important;
    border-color: #f5c542 !important;
    background: rgba(245,197,66,0.05) !important;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- ESTRUCTURA VISUAL ----------------

# 1. LOGO PRINCIPAL
st.markdown(f'<div style="text-align:center; margin-bottom:30px;"><img src="{LOGO}" width="180"></div>', unsafe_allow_html=True)

# 2. BIENVENIDA (CLON DE LA IMAGEN 2)
st.markdown("""
<div class="welcome-container">
    <div class="welcome-title">¡BIENVENIDO A <span>FOXE ARENA</span>!</div>
    <div class="welcome-subtitle">
        Siente la pasión del mundial, haz tus pronósticos<br>
        y vibra con la <b>banda sonora oficial</b>.
    </div>
    
</div>
""", unsafe_allow_html=True)

# 3. SECCIÓN MÚSICA
st.markdown("""
<div class="music-header">
    <div style="color:#f5c542; font-size:24px;">♫</div>
    <div class="section-label">BANDA SONORA OFICIAL</div>
    <div style="font-size:12px; color:gray;">Las últimas canciones añadidas a la porra</div>
</div>
""", unsafe_allow_html=True)

# 4. CARD DINÁMICA
songs = load_songs()
if not songs.empty:
    # Mostramos la última canción añadida (fila 0 o la última según tu sheet)
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

