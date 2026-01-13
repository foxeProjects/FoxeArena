import streamlit as st
import pandas as pd
import re

# ---------------- CONFIG ----------------
st.set_page_config(page_title="FOXE ARENA", page_icon="🎵", layout="centered")

SHEET_ID = "1HBGfa4EygznWWdKk3CkcM-THGGsUDp6W"
SONGS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=wc-songs"
USERS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=wc-user"

LOGO = "https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/assets/6516920E-25CA-423F-AD08-57D6C48BDDE1.png"
ESTADIO = "https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/assets/8B390EC8-EB25-48F3-8838-76DE0F4416D9.png"

# ---------------- HELPERS ----------------
def get_video_id(url):
    patterns = [
        r"youtu\.be\/([^?&]+)",
        r"youtube\.com\/watch\?v=([^?&]+)",
        r"youtube\.com\/embed\/([^?&]+)"
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None

def get_thumbnail(url):
    vid = get_video_id(url)
    if vid:
        return f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
    return ""

@st.cache_data(ttl=30)
def load_songs():
    return pd.read_csv(SONGS_URL)

@st.cache_data(ttl=30)
def load_users():
    return pd.read_csv(USERS_URL)

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
  font-family: 'Inter', sans-serif;
  color: #f5f5f5;
}}

.block-container {{
  max-width: 420px;
  padding-top: 20px;
}}

a {{ color: #f5c542 !important; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}

.logo-top {{
  display:flex;
  justify-content:center;
  margin-bottom: 10px;
}}
.logo-top img {{
  width: 120px;
  filter: drop-shadow(0 0 15px rgba(245,197,66,0.4));
}}

.header {{
  text-align: center;
  margin-bottom: 20px;
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
  background: rgba(0,0,0,0.6);
  box-shadow: 0 0 30px rgba(245,197,66,0.35);
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
  background: red;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 12px 30px rgba(0,0,0,0.6);
  transition: transform 0.2s ease;
}}

.play:hover {{
  transform: translate(-50%, -50%) scale(1.05);
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
  margin-top: 40px;
  font-size: 12px;
  color: rgba(255,255,255,0.35);
}}
.footer img {{
  width: 34px;
  margin-bottom: 6px;
}}

.admin-link {{
  margin-top: 10px;
  font-size: 13px;
  color: rgba(255,255,255,0.6);
  cursor: pointer;
}}
.admin-link:hover {{
  color: #f5c542;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------

songs = load_songs()

# LOGO
st.markdown(f"""
<div class="logo-top">
  <img src="{LOGO}">
</div>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="header">
  <div class="header-title">BANDA SONORA OFICIAL</div>
  <div class="header-sub">Las últimas canciones añadidas a la porra</div>
</div>
""", unsafe_allow_html=True)

# HOME
if st.session_state.view == "home":
    if not songs.empty:
        row = songs.iloc[0]
        thumb = get_thumbnail(row["url"])

        st.markdown(f"""
        <div class="video-card">
          <a href="{row["url"]}" target="_blank">
            <div class="video-thumb">
              <img src="{thumb}">
              <div class="play"></div>
            </div>
          </a>
          <div class="video-meta">
            <div class="video-title">{row["nombre"]}</div>
            <div class="video-sub">{row["grupo"]}</div>
            <a href="{row["url"]}" target="_blank">Ver en YouTube</a>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="footer">
      <img src="{LOGO}"><br>
      © 2026 FOXE ARENA. Todos los derechos reservados.
      <div class="admin-link" onclick="window.location.reload()">Admin Portal</div>
    </div>
    """, unsafe_allow_html=True)

# LOGIN VIEW (separada)
elif st.session_state.view == "login":
    st.markdown("### Admin Portal")

    with st.form("login"):
        u = st.text_input("User")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Entrar"):
            users = load_users()
            match = users[(users["user"] == u) & (users["password"] == p)]
            if not match.empty:
                st.session_state.is_admin = True
                st.success("Login OK")
                st.session_state.view = "home"
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
