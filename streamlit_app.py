import streamlit as st

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="FOXE ARENA",
    page_icon="🎵",
    layout="centered"
)

LOGO = "https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/assets/6516920E-25CA-423F-AD08-57D6C48BDDE1.png"
ESTADIO = "https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/assets/8B390EC8-EB25-48F3-8838-76DE0F4416D9.png"

# ---------------- CSS EXACTO ----------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

:root {{
  --gold: #f5c542;
  --gold-soft: rgba(245,197,66,0.45);
  --text-main: #f5f5f5;
  --text-muted: rgba(255,255,255,0.55);
}}

header {{ visibility: hidden; height: 0; }}

.stApp {{
  background:
    linear-gradient(rgba(0,0,0,0.82), rgba(0,0,0,0.95)),
    url("{ESTADIO}");
  background-size: cover;
  background-position: center;
  font-family: 'Inter', sans-serif;
  color: var(--text-main);
}}

.block-container {{
  max-width: 420px;
  padding-top: 24px;
  padding-bottom: 40px;
}}

a {{
  color: var(--gold);
  text-decoration: none;
}}

a:hover {{
  text-decoration: underline;
}}

/* ---------- HEADER ---------- */
.header {{
  text-align: center;
  margin-bottom: 24px;
}}

.header-icon {{
  font-size: 28px;
  color: var(--gold);
  margin-bottom: 6px;
}}

.header-title {{
  font-size: 28px;
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--gold);
}}

.header-sub {{
  font-size: 14px;
  color: var(--text-muted);
  margin-top: 6px;
}}

/* ---------- CARD ---------- */
.video-card {{
  border: 2px solid var(--gold);
  border-radius: 22px;
  overflow: hidden;
  background: rgba(0,0,0,0.55);
  box-shadow: 0 0 28px rgba(245,197,66,0.25);
}}

.video-thumb {{
  position: relative;
}}

.video-thumb img {{
  width: 100%;
  display: block;
}}

.play-button {{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 78px;
  height: 78px;
  background: #ff0000;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 14px 30px rgba(0,0,0,0.6);
}}

.play-button:before {{
  content: "";
  margin-left: 4px;
  width: 0;
  height: 0;
  border-left: 20px solid white;
  border-top: 14px solid transparent;
  border-bottom: 14px solid transparent;
}}

/* ---------- META ---------- */
.video-meta {{
  padding: 18px 18px 20px 18px;
}}

.video-title {{
  font-size: 20px;
  font-weight: 700;
  color: var(--gold);
  margin: 0;
}}

.video-sub {{
  font-size: 14px;
  color: var(--text-muted);
  margin-top: 4px;
}}

.video-link {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 10px;
  font-size: 14px;
  color: var(--gold);
}}

/* ---------- FOOTER ---------- */
.footer {{
  text-align: center;
  margin-top: 48px;
  font-size: 12px;
  color: rgba(255,255,255,0.35);
}}

.footer img {{
  width: 36px;
  margin-bottom: 6px;
  opacity: 0.9;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------

st.markdown("""
<div class="header">
  <div class="header-icon">🎵</div>
  <div class="header-title">BANDA SONORA OFICIAL</div>
  <div class="header-sub">Las últimas canciones añadidas a la porra</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="video-card">
  <div class="video-thumb">
    <img src="https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg">
    <div class="play-button"></div>
  </div>
  <div class="video-meta">
    <div class="video-title">Baila Baila</div>
    <div class="video-sub">Himno Foxe Arena</div>
    <a class="video-link" href="#" target="_blank">🔗 Ver en YouTube</a>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="footer">
  <img src="{LOGO}"><br>
  © 2026 FOXE ARENA. Todos los derechos reservados.
</div>
""", unsafe_allow_html=True)
