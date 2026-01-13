import streamlit as st
import pandas as pd
import re

# ---------------- CONFIG ----------------
st.set_page_config(page_title="FOXE ARENA", page_icon="🎵", layout="centered")

SHEET_ID = "1HBGfa4EygznWWdKk3CkcM-THGGsUDp6W"
SONGS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=wc-songs"
USERS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=wc-user"

# ✅ LOGO CORRECTO (el que pediste)
LOGO = "https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/assets/IMG_9234.png"
ESTADIO = "https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/assets/8B390EC8-EB25-48F3-8838-76DE0F4416D9.png"

# ---------------- HELPERS ----------------
def get_video_id(url: str):
    if not isinstance(url, str):
        return None
    patterns = [
        r"youtu\.be\/([^?&]+)",
        r"youtube\.com\/watch\?v=([^?&]+)",
        r"youtube\.com\/embed\/([^?&]+)",
        r"youtube\.com\/shorts\/([^?&]+)",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None

def get_thumbnail(url: str) -> str:
    vid = get_video_id(url)
    return f"https://img.youtube.com/vi/{vid}/hqdefault.jpg" if vid else ""

@st.cache_data(ttl=30)
def load_songs():
    df = pd.read_csv(SONGS_URL)
    # Normaliza nombres de columnas por si hay espacios raros
    df.columns = [c.strip().lower() for c in df.columns]
    return df

@st.cache_data(ttl=30)
def load_users():
    df = pd.read_csv(USERS_URL)
    df.columns = [c.strip().lower() for c in df.columns]
    return df

# ---------------- SESSION ----------------
if "view" not in st.session_state:
    st.session_state.view = "home"

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# ---------------- CSS ----------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

header {{ visibility: hidden; height: 0; }}

.stApp {{
  background:
    linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)),
    url("{ESTADIO}");
  background-size: cover;
  background-position: center;
  font-family: 'Inter', sans-serif;
  color: #f5f5f5;
}}

.block-container {{
  max-width: 420px;
  padding-top: 18px;
  padding-bottom: 30px;
}}

a {{
  color: #f5c542 !important;
  text-decoration: none !important;
}}
a:hover {{
  text-decoration: underline !important;
}}

.logo-top {{
  display:flex;
  justify-content:center;
  margin: 6px 0 14px 0;
}}
.logo-top img {{
  width: 160px;
  max-width: 72vw;
  height: auto;
  filter: drop-shadow(0 0 18px rgba(245,197,66,0.38));
}}

.header {{
  text-align: center;
  margin-bottom: 18px;
}}

.header-title {{
  font-size: 26px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #f5c542;
}}

.header-sub {{
  font-size: 14px;
  color: rgba(255,255,255,0.55);
}}

.video-card {{
  border: 2px solid #f5c542;
  border-radius: 22px;
  overflow: hidden;
  background: rgba(0,0,0,0.62);
  box-shadow: 0 0 32px rgba(245,197,66,0.33);
}}

.video-thumb {{
  position: relative;
}}

.video-thumb img {{
  width: 100%;
  display: block;
}}

.play {{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
  background: #ff0000;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 12px 30px rgba(0,0,0,0.6);
  transition: transform .18s ease;
}}

.play:hover {{
  transform: translate(-50%, -50%) scale(1.06);
}}

.play:before {{
  content: "";
  margin-left: 4px;
  border-left: 20px solid white;
  border-top: 14px solid transparent;
  border-bottom: 14px solid transparent;
}}

.video-meta {{
  padding: 18px;
}}

.video-title {{
  font-size: 20px;
  font-weight: 700;
  color: #f5c542;
}}

.video-sub {{
  font-size: 14px;
  color: rgba(255,255,255,0.6);
  margin-top: 4px;
}}

.footer {{
  text-align: center;
  margin-top: 34px;
  font-size: 12px;
  color: rgba(255,255,255,0.35);
}}

.footer img {{
  width: 34px;
  margin-bottom: 8px;
  opacity: .95;
  filter: drop-shadow(0 0 12px rgba(0,0,0,0.55));
}}

.footer-admin {{
  margin-top: 10px;
  color: rgba(255,255,255,0.45);
  font-size: 12px;
}}

.footer-admin .stButton>button {{
  background: transparent !important;
  border: none !important;
  color: rgba(255,255,255,0.45) !important;
  font-size: 12px !important;
  padding: 0 !important;
  height: auto !important;
}}
.footer-admin .stButton>button:hover {{
  color: #f5c542 !important;
  text-decoration: underline !important;
}}

.login-card {{
  border: 1px solid rgba(245,197,66,0.35);
  border-radius: 18px;
  padding: 16px;
  background: rgba(0,0,0,0.55);
  box-shadow: 0 0 22px rgba(245,197,66,0.18);
}}

.login-title {{
  font-size: 18px;
  font-weight: 700;
  color: #f5c542;
  margin-bottom: 10px;
}}

.stTextInput>div>div {{
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(245,197,66,0.22) !important;
  border-radius: 12px !important;
}}

.stButton>button {{
  background: linear-gradient(180deg,#f5c542,#c4972f) !important;
  color: #101010 !important;
  border-radius: 16px !important;
  border: none !important;
  height: 44px !important;
  font-weight: 700 !important;
  width: 100% !important;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
songs = load_songs()

# ---------------- TOP LOGO ----------------
st.markdown(f"""
<div class="logo-top">
  <img src="{LOGO}">
</div>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="header">
  <div class="header-title">BANDA SONORA OFICIAL</div>
  <div class="header-sub">Las últimas canciones añadidas a la porra</div>
</div>
""", unsafe_allow_html=True)

# ===================== VIEWS =====================

# -------- HOME --------
if st.session_state.view == "home":
    if not songs.empty:
        # por defecto: primera fila (si quieres "la última", te lo cambio a songs.iloc[-1])
        row = songs.iloc[0]
        nombre = str(row.get("nombre", "")).strip()
        grupo = str(row.get("grupo", "")).strip()
        url = str(row.get("url", "")).strip()

        thumb = get_thumbnail(url)

        st.markdown(f"""
        <div class="video-card">
          <a href="{url}" target="_blank">
            <div class="video-thumb">
              <img src="{thumb}">
              <div class="play"></div>
            </div>
          </a>
          <div class="video-meta">
            <div class="video-title">{nombre}</div>
            <div class="video-sub">{grupo}</div>
            <a href="{url}" target="_blank">Ver en YouTube</a>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # footer + admin portal
    st.markdown(f"""
    <div class="footer">
      <img src="{LOGO}"><br>
      © 2026 FOXE ARENA. Todos los derechos reservados.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="footer-admin">', unsafe_allow_html=True)
    if st.button("Admin Portal"):
        st.session_state.view = "login"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -------- LOGIN --------
elif st.session_state.view == "login":
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">Admin Portal</div>', unsafe_allow_html=True)

    with st.form("login_form"):
        u = st.text_input("User")
        p = st.text_input("Password", type="password")
        ok = st.form_submit_button("Entrar")

    if ok:
        users = load_users()
        match = users[(users["user"] == u) & (users["password"] == p)]
        if not match.empty and str(match.iloc[0].get("role","")).strip().lower() == "admin":
            st.session_state.is_admin = True
            st.session_state.view = "admin"
            st.success("✅ Login OK")
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

    # volver
    if st.button("← Volver"):
        st.session_state.view = "home"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# -------- ADMIN (placeholder visual, sin escritura aún) --------
elif st.session_state.view == "admin":
    if not st.session_state.is_admin:
        st.session_state.view = "login"
        st.rerun()

    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">Admin Portal</div>', unsafe_allow_html=True)
    st.write("✅ Entraste como admin. (Si quieres: aquí ponemos añadir/borrar canciones con tu misma estética.)")

    if st.button("Cerrar sesión"):
        st.session_state.is_admin = False
        st.session_state.view = "home"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
