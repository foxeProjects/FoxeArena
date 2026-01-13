import streamlit as st
import pandas as pd
import re

# ---------------- CONFIG ----------------
st.set_page_config(page_title="FOXE ARENA", page_icon="⚽️", layout="centered")

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
    # Usamos hqdefault.jpg por defecto porque siempre existe y evita el recuadro gris
    return f"https://img.youtube.com/vi/{vid}/hqdefault.jpg" if vid else ""

@st.cache_data(ttl=30)
def load_songs():
    try:
        df = pd.read_csv(SONGS_URL)
        df.columns = [c.strip().lower() for c in df.columns]
        return df
    except: return pd.DataFrame()

# ---------------- CSS (LIMPIEZA Y AJUSTE DE IMAGEN) ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');

/* Ocultar elementos Streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stHeader"] {visibility: hidden; height: 0;}
[data-testid="stDecoration"] {display: none !important;}

/* FONDO */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.85)), url("https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/assets/8B390EC8-EB25-48F3-8838-76DE0F4416D9.png");
    background-size: cover;
    background-position: center;
}

.block-container { 
    max-width: 450px; 
    padding-top: 1.5rem !important; 
}

/* BIENVENIDA */
.welcome-container { text-align: center; margin-bottom: 10px; }
.welcome-title { font-size: 30px; font-weight: 900; color: #FFFFFF; text-transform: uppercase; }
.welcome-title span { color: #f5c542; text-shadow: 0 0 15px rgba(245,197,66,0.7); }

/* SECCIÓN MÚSICA */
.music-header { text-align: center; padding-top: 5px; }
.section-label { font-size: 24px; font-weight: 800; color: #f5c542; letter-spacing: 1px; }

/* CARD VIDEO */
.video-card {
    background: rgba(20, 20, 20, 0.95);
    border: 2px solid #f5c542;
    border-radius: 22px;
    overflow: hidden;
    margin-top: 15px;
}
.thumb-container { 
    position: relative; 
    width: 100%; 
    aspect-ratio: 16/9; 
    background: #000;
    overflow: hidden;
}
.thumb-img { 
    width: 100%; 
    height: 100%; 
    object-fit: cover; /* Esto elimina las bandas negras de los lados */
}
.play-btn {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 60px; height: 60px;
    background: #ff0000;
    border-radius: 50%;
    display: flex; justify-content: center; align-items: center;
}
.play-btn::after {
    content: '';
    margin-left: 5px;
    border-left: 15px solid white;
    border-top: 10px solid transparent;
    border-bottom: 10px solid transparent;
}
.video-info { padding: 18px 22px; }
.v-title { font-size: 20px; font-weight: 700; color: #f5c542; }
.v-sub { color: #ffffff; font-size: 14px; margin-bottom: 10px; }
.v-link { color: #f5c542 !important; font-size: 12px; text-decoration: underline !important; }

/* FOOTER */
.footer-box { text-align: center; margin-top: 35px; padding-bottom: 25px; }
</style>
""", unsafe_allow_html=True)

# ---------------- ESTRUCTURA VISUAL ----------------

st.markdown(f'<div style="text-align:center; margin-bottom:15px;"><img src="{LOGO}" width="165"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="welcome-container">
    <div class="welcome-title">¡BIENVENIDO A <span>FOXE ARENA</span>!</div>
</div>
<div class="music-header">
    <div class="section-label">BANDA SONORA OFICIAL</div>
</div>
""", unsafe_allow_html=True)

songs = load_songs()
if not songs.empty:
    for index, row in songs.iterrows():
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

st.markdown(f"""
<div class="footer-box">
    <img src="{LOGO}" width="45"><br>
    <div style="font-size:10px; color:rgba(255,255,255,0.4);">© 2026 FOXE ARENA.</div>
</div>
""", unsafe_allow_html=True)
